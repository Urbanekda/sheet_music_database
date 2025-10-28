#!/bin/sh

# Create the log file if it doesn't exist
touch /var/log/cron.log

# Renew certificates
certbot renew --webroot -w /var/www/certbot --quiet

# Reload nginx to apply new certificates
echo "Reloading nginx..."
docker container exec frontend-proxy nginx -s reload