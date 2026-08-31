FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV HOME=/root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ca-certificates bash curl wget git nano vim less procps iproute2 iputils-ping openvpn iptables openssh-server && \
    curl -fsSL https://github.com/tsl0922/ttyd/releases/download/1.7.7/ttyd.x86_64 -o /usr/bin/ttyd && \
    chmod +x /usr/bin/ttyd && \
    curl -fL https://github.com/MasterAlanLab/free-proxy/releases/latest/download/free-proxy-linux-amd64 -o /usr/local/bin/free-proxy && \
    chmod +x /usr/local/bin/free-proxy && \
    ssh-keygen -A && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "root:unikraft" | chpasswd && \
    mkdir -p /root /data /run/sshd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config && \
    echo "ChallengeResponseAuthentication no" >> /etc/ssh/sshd_config && \
    echo "UsePAM yes" >> /etc/ssh/sshd_config && \
    echo "Subsystem sftp /usr/lib/openssh/sftp-server" >> /etc/ssh/sshd_config

COPY --chmod=755 wrapper.sh /usr/bin/wrapper.sh

ENTRYPOINT ["/usr/bin/wrapper.sh"]
