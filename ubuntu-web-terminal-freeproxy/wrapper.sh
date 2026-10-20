#!/bin/sh
export HOME=/root
export FREE_PROXY_DATA_DIR=/data/free-proxy
export TZ=Asia/Shanghai
mkdir -p "$FREE_PROXY_DATA_DIR"

# 后台启动 free-proxy 服务
nohup /usr/local/bin/free-proxy serve > /data/free-proxy.log 2>&1 &

# 前台运行 ttyd，保持容器存活
exec /usr/bin/ttyd -W -p 6080 -c root:unikraft /bin/bash
