FROM owasp/modsecurity-crs:3.3.4-nginx-alpine-202303180303
ARG OPENRESTY_VERSION=1.21.4.1
ARG CORERULESET_VERSION=3.3.4
RUN apk add --no-cache pv ca-certificates clamav clamav-libunrar perl && \
    mkdir -p /usr/local/clamav/rules
COPY ./modsec/coreruleset/crs.setup.conf /usr/local/coreruleset-${CORERULESET_VERSION}/crs.setup.conf

COPY ./modsec/modsecurity.conf /opt/ModSecurity/modsecurity.conf 
COPY ./modsec/main.conf /opt/ModSecurity/main.conf

COPY ./modsec/ClamAV/modsec_clamav.conf /usr/local/clamav/rules/modsec_clamav.conf
COPY ./modsec/ClamAV/modsec_clamav.pl /usr/local/clamav/rules/modsec_clamav.pl

RUN chmod +x /usr/local/clamav/rules/modsec_clamav.pl

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf

COPY ./nginx/conf.d /etc/nginx/conf.d
RUN cd /usr/local;\
    wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v${CORERULESET_VERSION}.tar.gz; \
    tar -xzvf v${CORERULESET_VERSION}.tar.gz; \
    mv coreruleset-${CORERULESET_VERSION}/ /usr/local; \
    cd /usr/local/coreruleset-${CORERULESET_VERSION}/; \
    cp crs-setup.conf.example crs-setup.conf; \
    cd /usr/local/coreruleset-${CORERULESET_VERSION}/rules; \
    mv REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf; \
    mv RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf


CMD ["nginx", "-g", "daemon off;"]