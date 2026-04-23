#!/bin/sh

REDIS_PASSWORD="${REDIS_PASSWORD:-unikraft}"

echo "requirepass $REDIS_PASSWORD" >> /etc/redis/redis.conf

exec /usr/bin/redis-server /etc/redis/redis.conf
