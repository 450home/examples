FROM node:24-bookworm

# Install sshd and other useful utilities
RUN apt-get update -y && apt-get install -y openssh-server vim jq rsync

# Install OpenClaw and the Unikraft Sandbox skill for OpenClaw
RUN npm i -g openclaw
RUN openclaw skills install unikraft-sandbox

COPY ./entrypoint.sh /usr/bin/entrypoint.sh
