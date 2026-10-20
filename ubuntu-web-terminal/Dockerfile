FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates bash curl wget git nano vim less procps iproute2 iputils-ping && \
    curl -fsSL https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -o /usr/bin/ttyd && \
    chmod +x /usr/bin/ttyd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "root:unikraft" | chpasswd && \
    mkdir -p /root /data

COPY --chmod=755 wrapper.sh /usr/bin/wrapper.sh

ENTRYPOINT ["/usr/bin/wrapper.sh"]
