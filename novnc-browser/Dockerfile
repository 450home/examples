FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    ca-certificates \
    xvfb \
    xterm \
    xdotool \
    scrot \
    openbox \
    x11vnc \
    tint2 \
    wget \
    firefox-esr && \
    update-ca-certificates && \
    apt-get purge -y man-db 2>/dev/null || true; \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /usr/share/doc/* /usr/share/man/* /usr/share/locale/* /var/cache/* /tmp/*

# Install noVNC via release tarballs (no git, no .git dirs)
RUN wget -qO /tmp/novnc.tgz https://github.com/novnc/noVNC/archive/refs/tags/v1.5.0.tar.gz && \
    wget -qO /tmp/websockify.tgz https://github.com/novnc/websockify/archive/refs/tags/v0.12.0.tar.gz && \
    mkdir -p /opt/noVNC/utils/websockify && \
    tar -xzf /tmp/novnc.tgz -C /opt/noVNC --strip-components=1 && \
    tar -xzf /tmp/websockify.tgz -C /opt/noVNC/utils/websockify --strip-components=1 && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html && \
    rm -f /tmp/novnc.tgz /tmp/websockify.tgz

COPY ./image /

COPY --chmod=755 ./wrapper.sh /wrapper.sh

ENTRYPOINT [ "/wrapper.sh" ]
