# HAProxy

This guide shows you how to use [HAProxy](https://www.haproxy.org).
HAProxy is a free and open source software that provides a high availability load balancer and reverse proxy for TCP and HTTP-based apps that spreads requests across many servers.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/haproxy/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/haproxy/
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
unikraft build . --output <my-org>/haproxy:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:8404/tls+http -m 256M --image <my-org>/haproxy:latest
```

or

```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:8404/tls+http -M 256Mi .
```

The output shows the instance address and other details:

```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: haproxy-rfx6z
 ├───────── uuid: 09bd081e-e082-4f73-8ba8-531123a39e2e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://cool-paper-svzzr3qq.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/haproxy@sha256:32296847231c151506820ec4914c1d7416e5b7200caf07c1e40eaa3ea5033d21
 ├─────── memory: 256 MiB
 ├────── service: cool-paper-svzzr3qq
 ├─ private fqdn: haproxy-rfx6z.internal
 └─── private ip: 10.0.6.5
```

or

```ansi title="unikraft"
metro:        fra
name:         haproxy-rfx6z
uuid:         09bd081e-e082-4f73-8ba8-531123a39e2e
state:        starting
image:        <my-org>/haproxy
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       c349833c-dacc-7763-306e-553f512c4d0e
  name:       cool-paper-svzzr3qq
  domains:
  - fqdn:     cool-paper-svzzr3qq.fra.unikraft.app
networks:
- uuid:       494814aa-38cc-c4ed-dcad-5b7173b3033b
  private-ip: 10.0.6.5
  mac:        12:b0:a4:a5:0d:24
timestamps:
  created:    just now
```

In this case, the instance name is `haproxy-rfx6z` and the address is `https://cool-paper-svzzr3qq.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the `/stats` endpoint (for example, `https://cool-paper-svzzr3qq.fra.unikraft.app/stats`).

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE             ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    haproxy-rfx6z  running  <my-org>/haproxy        256MiB  1      cool-paper-svzzr3qq.fra.unikraft.app  2 minutes ago
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME           FQDN                                  STATE    STATUS        IMAGE                                          MEMORY   VCPUS  ARGS  BOOT TIME
haproxy-rfx6z  cool-paper-svzzr3qq.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/haproxy@sha256:...  256 MiB  1            26.60 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete haproxy-rfx6z
```

or

```bash title="kraft"
kraft cloud instance remove haproxy-rfx6z
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
