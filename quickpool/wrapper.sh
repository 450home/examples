#!/bin/sh
set -ex

chown root:root /run/sshd 2>/dev/null || true
mkdir -p /root/.ssh /app/data
chmod 700 /root/.ssh

if [ -n "$PUBKEY" ]; then
    echo "$PUBKEY" > /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
fi

ssh-keygen -A >/dev/null 2>&1 || true

# quickpool: single worker, loopback only (reach it through the SSH tunnel or the edge)
QUICKPOOL_HOST=127.0.0.1 \
QUICKPOOL_PORT=8045 \
QUICKPOOL_CALLBACK_PORT=18080 \
QUICKPOOL_DATA_DIR=/app/data \
python3 -m quickpool > /app/data/quickpool.log 2>&1 &

sleep 3
echo "--- quickpool log ---"
cat /app/data/quickpool.log || true

/usr/sbin/sshd -D -h /etc/ssh/ssh_host_ecdsa_key -p 2222
