import sys
import yaml

def generate_suricata_rules(rules):
    generated_rules = []
    sid_counter = 10000001

    for rule in rules:
        rule_data = rule['rule']

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
    else:
        destination_ips_str = destination_ips.replace(',', ', ')

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
    
    output_rules_path = "my.rules"
    if len(sys.argv) >= 3:
        output_rules_path = sys.argv[2]

    with open(input_yaml_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)

    generated_rules = generate_suricata_rules(data['suricata'])

    with open(output_rules_path, 'w') as output_file:
        for rule_text in generated_rules:
            output_file.write(rule_text)

    print(f"Generated rules saved to {output_rules_path}")

if __name__ == "__main__":
    main()