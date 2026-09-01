#!/bin/sh
export HOME=/root
export TZ=Asia/Shanghai
mkdir -p /data/free-proxy /run/sshd /root/.ssh

# 数据持久化: free-proxy 固定用 /root/free_proxy_data，软链到持久卷
[ -e /root/free_proxy_data ] || ln -s /data/free-proxy /root/free_proxy_data

ssh-keygen -A
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config

if [ -n "$PUBKEY" ]; then
    echo "$PUBKEY" >> /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
fi

/usr/sbin/sshd -D -p 2222 &

# free-proxy (web 39527 / socks5+http 9527)
nohup /usr/local/bin/free-proxy serve > /data/free-proxy.log 2>&1 < /dev/null &

# socat 备用端口转发（Unikraft 内核无 iptables/nft）
socat TCP-LISTEN:9528,reuseaddr,fork TCP:127.0.0.1:9527 &
socat TCP-LISTEN:9529,reuseaddr,fork TCP:127.0.0.1:9527 &
socat TCP-LISTEN:9530,reuseaddr,fork TCP:127.0.0.1:9527 &

wait
