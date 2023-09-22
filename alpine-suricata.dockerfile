ARG ALPINE_VERSION=3.14.9

FROM alpine

#ENV container docker
## Install Suricata as describe here https://redmine.openinfosecfoundation.org/projects/suricata/wiki/Distributions_Containing_Suricata Repository : https://pkgs.alpinelinux.org/package/edge/community/x86/suricata
RUN apk update 
#RUN    apk add --no-cache --virtual  
#RUN    apk add suricata 
RUN    apk add iptables 
RUN    apk add python3 
RUN    apk add py3-pip; 
RUN    pip install suricata-update
RUN    pip install requests
RUN    apk add suricata

# Install Suricata-update utility https://github.com/OISF/suricata-update

COPY ./suricata/suricata-update.sh /etc/suricata/suricata-update.sh
# COPY file needed for the Suricata efficiency
COPY ./suricata/suricata-update-cron /etc/crontabs/suricata-update-cron
COPY ./suricata/docker-entrypoint.sh /tmp/docker-entrypoint.sh
COPY ./suricata/suricata.yaml /etc/suricata/suricata.yaml
COPY ./suricata/rules/generator.py /var/lib/suricata/rules/generator.py
COPY ./rules.yml /var/lib/suricata/rules/rules.yml
# Forwarding suricata application logs to stdout
RUN chmod +x /etc/crontabs/suricata-update-cron;\
    chmod +x /tmp/docker-entrypoint.sh;\
    chmod +x /var/lib/suricata/rules/generator.py;\
    chmod 400 /var/lib/suricata/rules/rules.yml
RUN python3 /var/lib/suricata/rules/generator.py /var/lib/suricata/rules/rules.yml /var/lib/suricata/rules/suricata.rules;\
    chmod 400 /var/lib/suricata/rules/suricata.rules
ENTRYPOINT [ "/tmp/docker-entrypoint.sh" ]
