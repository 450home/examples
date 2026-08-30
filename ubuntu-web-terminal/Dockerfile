FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates ttyd bash curl wget git nano vim less procps iproute2 iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "root:unikraft" | chpasswd && \
    mkdir -p /root /data

COPY --chmod=755 wrapper.sh /usr/bin/wrapper.sh

ENTRYPOINT ["/usr/bin/wrapper.sh"]
