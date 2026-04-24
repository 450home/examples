# Memcached

This guide shows you how to use [Memcached](https://memcached.org).
Memcached is an in-memory key-value store for small chunks of arbitrary data (strings, objects) from results of database calls, API calls, or page rendering.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/memcached1.6/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/memcached1.6/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/memcached1.6:latest
unikraft run --scale-to-zero policy=off --metro fra -p 11211:11211/tls -m 256M --image <my-org>/memcached1.6:latest
```

or

```bash title="kraft"
kraft cloud deploy --scale-to-zero off -p 11211:11211/tls -M 256Mi .
```

The output shows the instance address and other details:

```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: memcached16-arkv7
 ├───────── uuid: da436eca-bc64-46d7-a04c-72832652b10e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://weathered-smoke-hehsdinv.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/memcached16@sha256:f53cdbce4dc185e8acc8ecb93a0ab0ba99085ca0837a0ad2062aae9e31382e58
 ├─────── memory: 256 MiB
 ├────── service: weathered-smoke-hehsdinv
 ├─ private fqdn: memcached16-arkv7.internal
 └─── private ip: 10.0.6.5
```

or

```ansi title="unikraft"
metro:        fra
name:         memcached16-arkv7
uuid:         da436eca-bc64-46d7-a04c-72832652b10e
state:        starting
image:        <my-org>/memcached16
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       ce58c122-62e5-b82d-955d-63053dbc13ec
  name:       weathered-smoke-hehsdinv
  domains:
  - fqdn:     weathered-smoke-hehsdinv.fra.unikraft.app
networks:
- uuid:       1e9e37f9-1ba5-7c92-350e-f399db32d93d
  private-ip: 10.0.6.5
  mac:        12:b0:e3:15:81:6b
timestamps:
  created:    just now
```

In this case, the instance name is `memcached16-arkv7` which is different for each run.

To test the deployment, first forward the port with the `socat` command:

```bash
socat TCP-LISTEN:11211,reuseaddr,fork OPENSSL:weathered-smoke-hehsdinv.fra.unikraft.app:11211,verify=0
```

Now, on a separate console, run the following commands to test that it works (you should see output when incrementing):

```console
telnet 127.0.0.1 11211

set test 0 0 1
0

incr test 1

incr test 1
```

To exit telnet run:

```console
Ctrl + ]
Ctrl + C
```

To disconnect, kill the `socat` command with ctrl-C.

> **Note:**
> This guide uses `socat` for port forwarding only when a service doesn't support TLS and isn't HTTP-based (TLS/SNI determines the correct instance to send traffic to).
> Also note that port forwarding isn't needed when connecting via an instance's private IP/FQDN.
> For example, when a Memcached instance serves as a cache server to
> another instance that acts as a frontend and which **does** support TLS.

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME               STATE    IMAGE                 ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    memcached16-arkv7  running  <my-org>/memcached16        256MiB  1      weathered-smoke-hehsdinv.fra.unikraft…  2 minutes ago
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME               FQDN                                       STATE    STATUS          IMAGE                                              MEMORY   VCPUS  ARGS  BOOT TIME
memcached16-arkv7  weathered-smoke-hehsdinv.fra.unikraft.app  running  11 minutes ago  oci://unikraft.io/<my-org>/memcached16@sha256:...  256 MiB  1            19.27 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete memcached16-arkv7
```

or

```bash title="kraft"
kraft cloud instance remove memcached16-arkv7
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
