import sys
import yaml
import requests
def replace_first_rule(rule_text,rep_rule):
    lines = rule_text.split()
    
    if lines == []:
        return "#"
    if lines[0] != rep_rule and lines[0] != "#":
        if lines[0].startswith("#"):
            return "#"
        
        lines[0] = rep_rule
        
    return ' '.join(lines)

def generate_suricata_rules(rules):
    generated_rules = []
    sid_counter = 10000001

    
    for rule in rules:
        rule_data = rule['rule']

        if 'import' in rule_data:
            import_data = rule_data['import']
            rep_rule = rule_data['action']
            if 'url' in import_data:
                response = requests.get(import_data['url'])
                if response.status_code == 200:
                    imported_rules = response.text.split('\n')
                    for imported_rule in imported_rules:
                        imported_rule = replace_first_rule(imported_rule,rep_rule)
                        generated_rules.append(imported_rule)
            continue

        if isinstance(rule_data['action'], list):
            for action in rule_data['action']:
                generated_rule = generate_suricata_rule(rule_data, sid_counter, action)
                generated_rules.append(generated_rule)
                sid_counter += 1
        else:
            generated_rule = generate_suricata_rule(rule_data, sid_counter)
            generated_rules.append(generated_rule)
            sid_counter += 1

    return generated_rules

def generate_suricata_rule(rule, sid, action=None):
    template = '#{name}\n{action} {protocol} {source_ip} {source_port} -> {destination_ip} {destination_port} (msg:"{name}"; sid:{sid}; rev:{rev};)\n'

    if action is None:
        action = rule['action']

    destination_ips = rule['destination']['ip']
    if isinstance(destination_ips, list):
        destination_ips_str = ', '.join(destination_ips)
        destination_ips_str = f'[{destination_ips_str}]'
    else:
        destination_ips_str = destination_ips

    return template.format(
        name=rule['name'],
        action=action,
        protocol=rule['protocol'],
        source_ip=rule['source']['ip'],
        source_port=rule['source']['port'],
        destination_ip=destination_ips_str,
        destination_port=rule['destination']['port'],
        sid=sid,
        rev=rule.get('rev', 1)
    )

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <path_to_yaml_file> [output_file]")
        return

    input_yaml_path = sys.argv[1]
    
    output_rules_path = "generated_rules.txt"
    if len(sys.argv) >= 3:
        output_rules_path = sys.argv[2]

    with open(input_yaml_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    generated_rules = generate_suricata_rules(data['suricata'])

    with open(output_rules_path, 'w') as output_file:
        for rule_text in generated_rules:
            output_file.write(rule_text + '\n')

    print(f"Generated rules saved to {output_rules_path}")

if __name__ == "__main__":
    main()