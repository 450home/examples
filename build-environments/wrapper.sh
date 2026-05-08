#!/bin/sh

export PATH=/go/bin:/usr/local/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
export GOLANG_VERSION=1.26.1
export GOTOOLCHAIN=local
export GOPATH=/go

exec "$@"
