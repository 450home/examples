# Ubuntu Web Terminal + free-proxy

A lightweight Debian-based web terminal with [free-proxy](https://github.com/mastersir-lab/free-proxy) bundled for Unikraft Cloud, deployed to the Frankfurt (`fra`) metro.

## Access

- **Web Terminal**: Open the service URL in a browser and sign in with:
  - Username: `root`
  - Password: `unikraft`

- **free-proxy web admin** (after starting free-proxy):
  - URL: `https://<FQDN>:8443`

## Ports

| Port | Internal Port | Purpose |
| :--- | :--- | :--- |
| 443 | 6080 | ttyd Web Terminal |
| 8443 | 39527 | free-proxy Admin Panel |
| 9527 | 9527 | SOCKS5/HTTP Proxy |

## Image

`unikraft.io/iudd/ubuntu-web-terminal:freeproxy`
