#!/bin/bash
iptables -t nat -A PREROUTING -s 45.142.214.72 -p tcp --dport 443 -j DNAT --to-destination 94.198.218.15:443
iptables -t nat -A POSTROUTING -s 94.198.218.15 -p tcp --dport 443 -j SNAT --to-source 45.142.214.72


iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination 94.198.218.15:443
iptables -t nat -A POSTROUTING -d 94.198.218.15 -p tcp --dport 443 -j SNAT --to-source 77.95.11.7



iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 8080 -m state --state NEW -j DNAT --to 45.142.214.72:80
iptables -t nat -A PREROUTING -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -t nat -A POSTROUTING -p tcp -m tcp --dport 8080 j SNAT --to-source 45.142.214.72
