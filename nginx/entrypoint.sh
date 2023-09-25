#!/bin/sh
/bin/sh /hello.sh
# Проверяем, если директория /etc/letsencrypt/live/ пуста
if [ -z "$(ls -A /etc/letsencrypt/live/)" ]; then
    # Генерируем самоподписанный SSL-сертификат с помощью OpenSSL
    openssl req -new -newkey rsa:2048 -days 3650 -nodes -x509 \
        -subj "/CN=sni-support-required-for-valid-ssl" \
        -keyout /etc/letsencrypt/live/resty-auto-ssl-fallback.key \
        -out /etc/letsencrypt/live/resty-auto-ssl-fallback.crt             
fi

# if [ ! -s "/etc/apache2/.htpasswd" ]; then
#   mkdir -p /etc/apache2
#   htpasswd -b -c "/etc/apache2/.htpasswd" "$username" "$password"
# fi

# Запускаем Nginx
/usr/local/openresty/bin/openresty -g "daemon off;"
