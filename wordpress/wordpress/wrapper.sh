#!/usr/bin/env bash

set -e

# Wait for MariaDB to be ready
retries=0
max_retries=5
while ! mysql -h "$WORDPRESS_DB_HOST" -u root -punikraft -e "SELECT 1;" mysql > /dev/null 2>&1; do
  retries=$((retries+1))
  if [ "$retries" -ge "$max_retries" ]; then
    echo "ERROR: Could not connect to MariaDB at $WORDPRESS_DB_HOST after $max_retries attempts."
    exit 1
  fi
  echo "Waiting for MariaDB at $WORDPRESS_DB_HOST... (attempt $retries/$max_retries)"
  sleep 2
done

echo "Initializing database ..."
mysql -h "$WORDPRESS_DB_HOST" -u root -punikraft < /init.sql

echo "Copying WordPress files ..."
cp -r /var/www/html-tmp/* /var/www/html/

echo "Starting PHP FPM daemon..."
/usr/sbin/php-fpm8.2 --fpm-config /etc/php/8.2/fpm/php-fpm.conf
/usr/lib/php/php-fpm-socket-helper install /run/php/php-fpm.sock /etc/php/8.2/fpm/pool.d/www.conf 82

echo "Starting nginx ..."
/usr/sbin/nginx -c /etc/nginx/nginx.conf
