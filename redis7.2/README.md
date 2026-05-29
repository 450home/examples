# Redis

This guide shows you how to use [Redis](https://redis.io), an open source in-memory storage, used as a distributed, in-memory key–value database, cache and message broker, with optional durability.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/redis7.2/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/redis7.2/
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

When done, invoke the following command to deploy this app on Unikraft Cloud:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/redis72:latest
unikraft run --scale-to-zero policy=off --metro fra -p 6379:6379/tls -m 512M --image <my-org>/redis72:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero off -p 6379:6379/tls -M 512Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         redis72-alb4r
uuid:         d3c3141b-97b2-4e1d-87ae-39e4f14ab49e
state:        starting
image:        <my-org>/redis72
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       7a4f2b3c-1d8e-4a92-b3f5-e6c1d2a3b4e5
  name:       rough-wind-8vxrd1ms
  domains:
  - fqdn:     rough-wind-8vxrd1ms.fra.unikraft.app
networks:
- uuid:       9b5e1f8d-3c2a-7b46-d1e9-f2a3b4c5d6e7
  private-ip: 10.0.3.2
  mac:        12:b0:4e:20:b3:e7
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: redis72-alb4r
 ├───────── uuid: d3c3141b-97b2-4e1d-87ae-39e4f14ab49e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://rough-wind-8vxrd1ms.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/redis72@sha256:9665c51faf7deb538cf7907b012b55700cad08cd391f5ba099d95d018c8da7d
 ├─────── memory: 512 MiB
 ├────── service: rough-wind-8vxrd1ms
 ├─ private fqdn: redis72-alb4r.internal
 └─── private ip: 10.0.3.2
```

In this case, the instance name is `redis72-alb4r` which is different for every run.

To test the deployment, first forward the port using `socat`:

```bash
socat TCP-LISTEN:6379,fork OPENSSL:rough-wind-8vxrd1ms.fra.unikraft.app:6379,verify=0
```

Then, from another console, you can now use the `redis-benchmark` client to connect to Redis, for example:

```console
redis-benchmark -t ping,set,get -n 10000
```

You should see output like:

```ansi
====== PING_INLINE ======
  10000 requests completed in 32.03 seconds
  50 parallel clients
  3 bytes payload
  keep alive: 1
  host configuration "save":
  host configuration "appendonly": no
  multi-thread: no

0.01% <= 138 milliseconds
0.05% <= 139 milliseconds
2.34% <= 140 milliseconds
4.49% <= 141 milliseconds
8.57% <= 142 milliseconds
16.06% <= 143 milliseconds
21.83% <= 144 milliseconds
26.25% <= 145 milliseconds
34.54% <= 146 milliseconds
...
```

To disconnect, kill the `socat` command with ctrl-C.

> **Note:**
> This guide uses `socat` for port forwarding only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that port forwarding isn't needed when connecting via an instance's private IP/FQDN.
> For example, when a Redis instance serves as a cache server to
> another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE              ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    redis72-alb4r  running  <my-org>/redis72        512MiB  1      rough-wind-8vxrd1ms.fra.unikraft.app  1 minute ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME           FQDN                                  STATE    STATUS        IMAGE                                           MEMORY   VCPUS  ARGS  BOOT TIME
redis72-alb4r  rough-wind-8vxrd1ms.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/redis72@sha256:...  512 MiB  1            26.13 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete redis72-alb4r
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove redis72-alb4r
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

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
