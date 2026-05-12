# Flask + Redis HTTP Server

This guide explains how to create and deploy a [Flask](https://flask.palletsprojects.com/en/3.0.x/) app with a [Redis](https://redis.io/) database on Unikraft Cloud.
The example consists of two services: a Flask web server that increments a page view counter stored in Redis.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-flask-redis` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-flask-redis/
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

### Deploy Redis

First, deploy the Redis instance.
Redis is an internal service (not publicly accessible), reached via the `redis.internal` domain:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build redis/ --output <my-org>/redis:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -m 256M --image <my-org>/redis:latest --domain redis.internal
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -M 256Mi --domain redis.internal redis/
```

The output shows the Redis instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:         fra
name:          redis-09p2q
uuid:          0355f93a-7b60-4ade-9359-b01671e812b3
state:         starting
image:         <my-org>/redis
resources:
  memory:      256MiB
  vcpus:       1
service:
  uuid:        19c050b2-b5c9-4e8e-9d25-a9053ff09270
  name:        damp-brook-xmmmwzwo
  domains:
  - fqdn:      redis.internal
networks:
- uuid:        97df34f7-63bc-4f02-a1b4-5ba07278de00
  private-ip:  10.0.0.41
  mac:         12:b0:0a:00:00:29
timestamps:
  created:     just now
scale-to-zero: policy=idle,stateful=true,cooldown-time=1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: redis-o9abw
 ├───────── uuid: 9dd4c7b5-7cc4-4b99-ac70-b10af54ef075
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: redis.internal
 ├──────── image: oci://unikraft.io/<my-org>/redis@sha256:3e35bc6c8048269741a0c0b4b165a10112736c48dbf869c76bb263a237502462
 ├─────── memory: 256 MiB
 ├────── service: sparkling-fire-rnd4o9kb
 ├─ private fqdn: redis-o9abw.internal
 └─── private ip: 10.0.0.41
```

### Deploy Flask

Next, deploy the Flask web server.
It connects to Redis using the `REDIS_HOST` and `REDIS_PORT` environment variables:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build flask/ --output <my-org>/flask:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:8000/tls+http -m 512M --image <my-org>/flask:latest --env REDIS_HOST=redis.internal --env REDIS_PORT=6379
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:8000/tls+http -M 512Mi flask/ --env REDIS_HOST=redis.internal --env REDIS_PORT=6379
```

The output shows the Flask instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:          fra
name:           flask-q62qa
uuid:           d081ec92-629b-45b3-8caf-059e0a87dffd
state:          starting
image:          <my-org>/flask
runtime:
  env:
    REDIS_HOST: redis.internal
    REDIS_PORT: 6379
resources:
  memory:       512MiB
  vcpus:        1
service:
  uuid:         ac1cd90e-a1fe-478c-8f58-8598fa80c494
  name:         hidden-silence-htyml3s2
  domains:
  - fqdn:       hidden-silence-htyml3s2.fra.unikraft.app
networks:
- uuid:         d2f3d024-3082-4e98-be22-f36df84263a1
  private-ip:   10.0.0.53
  mac:          12:b0:0a:00:00:35
timestamps:
  created:      just now
scale-to-zero:  policy=on,cooldown-time=1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: flask-a06h2
 ├───────── uuid: 431f67ed-1f18-4dc1-86db-68dac4edff51
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://withered-cherry-xfcrfp93.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/flask@sha256:3d29ca3a8a3d434f41acf7c8093435836dcbacca9190c51ec39dbb4ddf1ee45a
 ├─────── memory: 512 MiB
 ├────── service: withered-cherry-xfcrfp93
 ├─ private fqdn: flask-a06h2.internal
 └─── private ip: 10.0.0.53
```

In this case, the Flask instance address is `https://withered-cherry-xfcrfp93.fra.unikraft.app`.
It's different for each run.

### Test the deployment

Use `curl` to query the Flask instance.
Each request increments the Redis counter:

```bash
curl https://withered-cherry-xfcrfp93.fra.unikraft.app
```

```text
This webpage has been viewed 1 time(s)
```

```bash
curl https://withered-cherry-xfcrfp93.fra.unikraft.app
```

```text
This webpage has been viewed 2 time(s)
```

You can list information about the instances by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

### Clean up

When done, remove the instances:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete flask-q62qa
unikraft instances delete redis-09p2q
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove flask-a06h2
kraft cloud instance remove redis-o9abw
```

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
