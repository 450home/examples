FROM python:3.12-slim

RUN set -xe; \
    apt-get update; \
    apt-get install -y --no-install-recommends openssh-server ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    mkdir -p /run/sshd /app/data /root/.ssh; \
    chmod 700 /root/.ssh

RUN pip install --no-cache-dir "https://github.com/avilliai/awsquick2api/archive/refs/heads/main.tar.gz"

COPY ./sshd_config /etc/ssh/sshd_config
COPY ./wrapper.sh /usr/bin/wrapper.sh
RUN chmod +x /usr/bin/wrapper.sh

ENV QUICKPOOL_HOST=127.0.0.1 \
    QUICKPOOL_PORT=8045 \
    QUICKPOOL_CALLBACK_PORT=18080 \
    QUICKPOOL_DATA_DIR=/app/data

EXPOSE 8045 18080 2222

CMD ["/usr/bin/wrapper.sh"]
