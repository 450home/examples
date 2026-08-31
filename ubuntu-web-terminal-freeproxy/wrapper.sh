#!/bin/sh
export HOME=/root
export FREE_PROXY_DATA_DIR=/data/free-proxy
export TZ=Asia/Shanghai
mkdir -p "$FREE_PROXY_DATA_DIR" /run/sshd

# 启动 SSH
if [ -n "$PUBKEY" ]; then
    echo "$PUBKEY" >> /root/.ssh/authorized_keys
fi
/usr/sbin/sshd -D -h /etc/ssh/ssh_host_ecdsa_key -p 2222 &
sleep 1

# 启动 free-proxy（web UI: 39527, proxy: 9527）
nohup /usr/local/bin/free-proxy serve > /data/free-proxy.log 2>&1 &
sleep 3

# 用 iptables 将 9528-9530 转发到 9527
iptables -t nat -A PREROUTING -p tcp --dport 9528 -j REDIRECT --to-port 9527
iptables -t nat -A PREROUTING -p tcp --dport 9529 -j REDIRECT --to-port 9527
iptables -t nat -A PREROUTING -p tcp --dport 9530 -j REDIRECT --to-port 9527

# 保持容器存活
tail -f /dev/null
