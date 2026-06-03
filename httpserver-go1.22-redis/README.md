# Go and Redis HTTP Server

This guide explains how to create and deploy a Go app with a Redis database.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-go1.22-redis` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-go1.22-redis/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft login
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

## Redis

First, deploy the Redis instance.
Redis is an internal service (not publicly accessible), reached via the `go122-redis.internal` domain.
The Redis password is set at runtime via the `REDIS_PASSWORD` environment variable (defaults to `unikraft` if not provided).

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./redis --output <my-org>/httpserver-go-122-redis-db:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -m 256M --image <my-org>/httpserver-go-122-redis-db:latest --domain go122-redis.internal -e REDIS_PASSWORD=unikraft
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -M 256Mi --domain go122-redis.internal --env REDIS_PASSWORD=unikraft ./redis/
```

Make sure to replace `<my-org>` with your username / org-name.

The output shows the Redis instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:           fra
name:            httpserver-go-122-redis-db-2xc9u
uuid:            8abe24f6-5670-4e9b-8955-8ec10f3bad21
state:           starting
image:           <my-org>/httpserver-go-122-redis-db
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          late-sound-rhboe98o
  uuid:          01953c15-8a2e-4c1a-ac24-98a9417c5aa2
  domains:
  - fqdn:        go122-redis.internal
networks:
- uuid:          e76ae319-d210-4566-ad75-baed32fc3d2b
  private-ip:    10.0.0.85
  mac:           12:b0:0a:00:00:55
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        idle
  stateful:      true
  cooldown-time: 1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-go-122-redis-db-2xc9u
 ├───────── uuid: 8abe24f6-5670-4e9b-8955-8ec10f3bad21
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: go122-redis.internal
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-go-122-redis-db@sha256:0b007ec2f56194da3a468aa93f4a2b8f267b1726ef3780355fbadb228fdf5c23
 ├─────── memory: 256 MiB
 ├────── service: late-sound-rhboe98o
 ├─ private fqdn: httpserver-go-122-redis-db-2xc9u.internal
 └─── private ip: 10.0.0.85
```

## Go HTTP Server

Next, deploy the Go HTTP server.
It connects to Redis using the `REDIS_ADDR` and `REDIS_PASS` environment variables:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./httpserver-go --output <my-org>/httpserver-go-122-redis-app:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:8080/tls+http -m 256M --image <my-org>/httpserver-go-122-redis-app:latest --env REDIS_ADDR=go122-redis.internal:6379 --env REDIS_PASS=unikraft
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 256Mi ./httpserver-go/ --env REDIS_ADDR=go122-redis.internal:6379 --env REDIS_PASS=unikraft
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:           fra
name:            httpserver-go-122-redis-app-bnnnc
uuid:            82093bcf-fc4c-471c-89c8-4d0b7810e280
state:           starting
image:           <my-org>/httpserver-go-122-redis-app
runtime:
  env:
    REDIS_ADDR:  go122-redis.internal:6379
    REDIS_PASS:  unikraft
resources:
  memory:        256MiB
  vcpus:         1
service:
  name:          frosty-cherry-32qs6na2
  uuid:          bcb9a2af-cfce-4731-9844-5a368696ee7d
  domains:
  - fqdn:        frosty-cherry-32qs6na2.fra.unikraft.app
networks:
- uuid:          f9030f74-4e85-445b-a57e-36ec76137c88
  private-ip:    10.0.0.173
  mac:           12:b0:0a:00:00:ad
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        on
  cooldown-time: 1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-go-122-redis-app-bnnnc
 ├───────── uuid: 82093bcf-fc4c-471c-89c8-4d0b7810e280
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://frosty-cherry-32qs6na2.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-go-122-redis-app@sha256:b923ac1ea60f83bdc61564aff95b11bac8a9e084f62532d0e882484d26e99da9
 ├─────── memory: 256 MiB
 ├────── service: frosty-cherry-32qs6na2
 ├─ private fqdn: httpserver-go-122-redis-app-bnnnc.internal
 └─── private ip: 10.0.0.173
```

In this case, the instance names are `httpserver-go-122-redis-db-2xc9u` and `httpserver-go-122-redis-app-bnnnc`.
They're different for each run.

To set a value in Redis via the Go server, use the URL from the `fqdn` field:

```bash
curl -X POST -d "key=my-key" -d "value=my-value" https://<FQDN>
```

```
Success!
```

You can then retrieve the value:

```bash
curl https://<FQDN>/?key=my-key
```

```
Key "my-key" has value "my-value"
```

You can list information about the instances by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                               STATE    IMAGE                                 ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-go-122-redis-app-bnnnc  standby  <my-org>/httpserver-go-122-redis-app        256MiB  1      frosty-cherry-32qs6na2.fra.unikraft.app  4 minutes ago
fra    httpserver-go-122-redis-db-2xc9u   standby  <my-org>/httpserver-go-122-redis-db         256MiB  1      go122-redis.internal                     5 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                               FQDN                                     STATE    STATUS        IMAGE                                                    MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-go-122-redis-app-bnnnc  frosty-cherry-32qs6na2.fra.unikraft.app  running  since 3secs   oci://unikraft.io/<my-org>/httpserver-go-122-redis-a...  256 MiB  1            968.01 ms
httpserver-go-122-redis-db-2xc9u   go122-redis.internal                     running  since 35secs  oci://unikraft.io/<my-org>/httpserver-go-122-redis-...   256 MiB  1            1707.20 ms
```

## Clean up

When done, remove the instances:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-go-122-redis-db-2xc9u httpserver-go-122-redis-app-bnnnc
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-go-122-redis-db-2xc9u httpserver-go-122-redis-app-bnnnc
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft --help
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
