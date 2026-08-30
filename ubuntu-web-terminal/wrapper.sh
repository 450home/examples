#!/bin/sh
export HOME=/root
mkdir -p /data
exec /usr/bin/ttyd -W -p 6080 -c root:unikraft /bin/bash
