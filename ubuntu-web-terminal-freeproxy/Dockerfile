FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/root

# ttyd Web 终端组件
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates bash curl wget git nano vim less procps iproute2 iputils-ping openvpn iptables && \
    curl -fsSL https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -o /usr/bin/ttyd && \
    chmod +x /usr/bin/ttyd && \
    # free-proxy 二进制
    curl -fL https://github.com/mastersir-lab/free-proxy/releases/latest/download/free-proxy-linux-amd64 -o /usr/local/bin/free-proxy && \
    chmod +x /usr/local/bin/free-proxy && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "root:unikraft" | chpasswd && \
    mkdir -p /root /data

COPY --chmod=755 wrapper.sh /usr/bin/wrapper.sh

ENTRYPOINT ["/usr/bin/wrapper.sh"]
