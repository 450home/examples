#!/bin/bash
set -ex

test -d /tmp || mkdir /tmp
chmod 1777 /tmp

export MYSQL_ROOT_HOST=%

exec bash -x /usr/local/bin/docker-entrypoint.sh mysqld \
  --user=root \
  --bind-address=0.0.0.0 \
  --innodb-buffer-pool-size=128M \
  --max-connections=50 \
  --table-definition-cache=400 \
  --table-open-cache=400
