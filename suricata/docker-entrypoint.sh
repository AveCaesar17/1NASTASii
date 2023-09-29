#!/bin/bash

# Update suricata rules
#suricata-update
#python3 /var/lib/suricata/rules/generator.py /var/lib/suricata/rules/rules.yml /var/lib/suricata/rules/suricata.rules
# Start cron
#crond
# Add cronjob
#crontab /etc/crontabs/suricata-update-cron
sudo /sbin/iptables -t mangle -I PREROUTING -p tcp -m tcp -m mark ! --mark 0x1/0x1 -j NFQUEUE --queue-num 0 --queue-bypass
sudo /sbin/iptables -I INPUT -j NFQUEUE --queue-bypass
sudo /sbin/iptables -I OUTPUT -j NFQUEUE --queue-bypass
# Started suricata
#rm -r /etc/suricata/rules/
exec /bin/bash -c "sudo /usr/bin/suricata -c /etc/suricata/suricata.yaml -q 0 -v"
