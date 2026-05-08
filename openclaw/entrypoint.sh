#!/usr/bin/bash

set -ex

# Start SSH server.
export HOME=/root

if test ! -z "$PUBKEY"; then
    mkdir -p /root/.ssh
    touch /root/.ssh/authorized_keys
    echo "$PUBKEY" >> /root/.ssh/authorized_keys
fi

mkdir -p /run/sshd
/usr/sbin/sshd -D -h /etc/ssh/ssh_host_ecdsa_key -p 2222
