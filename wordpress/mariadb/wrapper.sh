#!/bin/sh

set -e

test -d /tmp || mkdir /tmp
chmod 1777 /tmp
/usr/local/bin/docker-entrypoint.sh mariadbd
