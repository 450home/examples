#!/usr/bin/env bash

export HOME=/
export DEBIAN_FRONTEND=noninteractive
export DEBIAN_PRIORITY=high
export DISPLAY_NUM=1
export HEIGHT=768
export WIDTH=1024

# Debug mode: sshd + hang forever, for diagnosing Xvfb failures over SSH
if [ "$DEBUG_HOLD" = "1" ]; then
    export PATH=$PATH:/usr/sbin
    mkdir -p /run/sshd /root/.ssh
    [ -n "$PUBKEY" ] && echo "$PUBKEY" >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys
    echo "root:unikraft" | chpasswd 2>/dev/null || true
    /usr/sbin/sshd -D -p 2222 &
    echo "DEBUG_HOLD: container stays alive for SSH diagnosis"
    exec sleep infinity
fi

set -e

# Start dependencies
./start_all.sh

# Start noVNC with explicit websocket settings
/opt/noVNC/utils/novnc_proxy \
    --vnc 0.0.0.0:5900 \
    --listen 6080 \
    --web /opt/noVNC
