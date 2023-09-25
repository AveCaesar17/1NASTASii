import yaml
import argparse
import os
import sys


def create_file(nginx_config, output_file): 
    with open(f"/usr/local/openresty/nginx/{output_file}", "w") as f:
        f.write(nginx_config)
    return nginx_config

def generate_nginx_config(data):
    if "config" in data:
        for item in data["config"]:
            if list(item.keys())[0] == 'route':
                nginx_config = generate_route(item,data)
                
            if list(item.keys())[0] == 'proxy':
                nginx_config = generate_proxy(item,data)
    else:
        print("Файл не заполнен")
        
    
    return nginx_config
def generate_proxy(proxy,data):
    nginx_config = ""
    nginx_config += f"upstream {proxy['proxy']['name']} {{\n"
    for item in proxy["proxy"]["endpoint"]["upstream"]:
        for upstream in item['hosts']: 
            for host in data['hosts']: 
                if host["host"]["name"] == upstream:
                    for ip in host['host']['ip']:
                        for service in host['host']['services']:
                            if service["service"]["name"] == item['service']:
                                upstream_config = f"         server {ip}:{service['service']['port']};\n" 
                                nginx_config += upstream_config 
    if "options" in item:
        for option in item['options']:
            for param in option.keys():
                nginx_config +=f"         {param} {option[param]};\n"
    nginx_config += "}\n" 
    nginx_config += "server {\n"
    nginx_config += f"    listen {proxy['proxy']['destination']['port']}"
    if "ssl" in proxy['proxy']['endpoint']: 
        nginx_config += " ssl;\n"
        ssl_config = ""
        if "ssl_certificate" in proxy['proxy']['endpoint']['ssl']:
        
            with open(f"{os.getcwd()}/{proxy['proxy']['endpoint']['ssl']['ssl_certificate']}", "r") as f:
                read_data = f.read()
            output_file = f"certs/{str(proxy['proxy']['name']).replace(' ','_')}/{str(proxy['proxy']['name']).replace(' ','_')}.crt"
            create_file(read_data,output_file)
            ssl_config += f"    ssl_certificate {output_file};\n"
        if "ssl_certificate_key" in proxy['proxy']['endpoint']['ssl']:
            with open(f"{os.getcwd()}/{proxy['proxy']['endpoint']['ssl']['ssl_certificate_key']}", "r") as f:
                read_data = f.read()
            output_file = f"certs/{str(proxy['proxy']['name']).replace(' ','_')}/{str(proxy['proxy']['name']).replace(' ','_')}.key"
            create_file(read_data,output_file)
            ssl_config += f"    ssl_certificate {proxy['proxy']['endpoint']['ssl']['ssl_certificate_key']}"
        nginx_config += ssl_config
    nginx_config += ";\n"
    if "hostname" in proxy['proxy']['endpoint']:
        nginx_config += f"    server_name {proxy['proxy']['endpoint']['hostname']};\n"
    for location in proxy['proxy']['endpoint']['url']: 
        nginx_config += f"\n    location {location['path']} {{\n"
        if 'options' in location:
            for option in location['options']:
                for param in option.keys():
                    nginx_config += f"       {param} {option[param]};\n"
        for host_pass in proxy['proxy']['endpoint']['upstream']:
            if host_pass['id'] == location['upstream_group']:
                if host_pass['ssl'] is True:
                    nginx_config += f"       proxy_pass https://{proxy['proxy']['name']};\n"
                else:
                    nginx_config += f"       proxy_pass http://{proxy['proxy']['name']};\n"
                nginx_config += "   }\n"
    nginx_config += "}\n"  
            
                                    

    output_file = f"conf/conf.d/{str(proxy['proxy']['name']).replace(' ','_')}/{str(proxy['proxy']['name']).replace(' ','_')}.conf"
    create_file(nginx_config,output_file)
         
        
def generate_route(route,data):
    nginx_config = ""
    forward_host = route["route"]["endpoint"]["host"]
    forward_service = route["route"]["endpoint"]["service"]
    for host in data["hosts"]:
        if host["host"]["name"] == forward_host:
                nginx_config += f"upstream {host['host']['name']}_{forward_service} {{\n"
                for ip in host["host"]["ip"]: 
                    for service in host["host"]["services"]:
                        if service["service"]["name"] == route["route"]["endpoint"]["service"]:
                            upstream = f"        server {ip}:{service['service']['port']};\n"    
                            nginx_config += upstream
                            if route['route']['protocol'] == 'tcp' or route['route']['protocol'] == 'http':
                                server = f"    listen {route['route']['destination']['port']};\n"
                            elif route['route']['protocol'] == 'udp':
                                server = f"    listen {route['route']['destination']['port']} udp;\n"
                proxy_pass = f"    proxy_pass {host['host']['name']}_{forward_service};\n"
                nginx_config += "}\n"
                nginx_config += f"server {{\n"
                nginx_config += server
                nginx_config += proxy_pass
                nginx_config += f"}}\n\n"
    
    output_file = f"conf/stream/{str(route['route']['name']).replace(' ','_')}/{str(route['route']['name']).replace(' ','_')}.conf"
    create_file(nginx_config,output_file)
    

def main():
    parser = argparse.ArgumentParser(description="Generate Nginx config from YAML input file")
    parser.add_argument("input_file", help="Path to the input YAML file")
    args = parser.parse_args()

    input_file = args.input_file
    path = str(sys.argv[1])[:str(sys.argv[1]).rfind("/")]
    os.chdir(path)
    with open(input_file, "r") as f:
        yaml_data = yaml.safe_load(f)

    generate_nginx_config(yaml_data)

   

if __name__ == "__main__":
    
    
    main()