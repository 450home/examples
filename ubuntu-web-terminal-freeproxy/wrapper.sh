#!/bin/sh
export HOME=/root
export FREE_PROXY_DATA_DIR=/data/free-proxy
export TZ=Asia/Shanghai
mkdir -p "$FREE_PROXY_DATA_DIR" /run/sshd /root/.ssh

# 生成 SSH 主机密钥（如果缺失）
ssh-keygen -A

# 配置 SSH：允许 root 密码登录
sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# 导入公钥
if [ -n "$PUBKEY" ]; then
    echo "$PUBKEY" >> /root/.ssh/authorized_keys
    chmod 600 /root/.ssh/authorized_keys
fi

# 启动 SSH，后台运行，保持前台
/usr/sbin/sshd -D -p 2222 &

# 等待 SSH 就绪
sleep 2
ss -tlnp | grep :2222 || echo "WARN: SSH may not be listening on 2222"

# 启动 free-proxy（web UI: 39527, proxy: 9527）
nohup /usr/local/bin/free-proxy serve > /data/free-proxy.log 2>&1 &
sleep 3

# 用 iptables 将 9528-9530 转发到 9527
iptables -t nat -A PREROUTING -p tcp --dport 9528 -j REDIRECT --to-port 9527
iptables -t nat -A PREROUTING -p tcp --dport 9529 -j REDIRECT --to-port 9527
iptables -t nat -A PREROUTING -p tcp --dport 9530 -j REDIRECT --to-port 9527

# 保持容器存活
wait
