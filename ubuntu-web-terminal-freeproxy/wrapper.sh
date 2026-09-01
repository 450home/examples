#!/bin/sh
export HOME=/root
export FREE_PROXY_DATA_DIR=/data/free-proxy
export TZ=Asia/Shanghai
mkdir -p "$FREE_PROXY_DATA_DIR" /run/sshd /root/.ssh

# 生成 SSH 主机密钥（如果缺失）
ssh-keygen -A

# 配置 SSH：允许 root 登录
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# 导入公钥
if [ -n "$PUBKEY" ]; then
    echo "$PUBKEY" >> /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
fi

# 启动 SSH
/usr/sbin/sshd -D -p 2222 &

# 启动 free-proxy（web UI: 39527, proxy: 9527）
nohup /usr/local/bin/free-proxy serve > /data/free-proxy.log 2>&1 &
sleep 3

# 用 socat 把 9528-9530 转发到 9527（用户态，无内核依赖）
# iptables/nft 在 Unikraft 内核不可用
pkill socat 2>/dev/null
socat TCP-LISTEN:9528,bind=0.0.0.0,reuseaddr,fork TCP:127.0.0.1:9527 &
socat TCP-LISTEN:9529,bind=0.0.0.0,reuseaddr,fork TCP:127.0.0.1:9527 &
socat TCP-LISTEN:9530,bind=0.0.0.0,reuseaddr,fork TCP:127.0.0.1:9527 &

# 保持容器存活
wait
