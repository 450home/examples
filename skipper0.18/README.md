# Skipper

This example uses [`Skipper`](https://opensource.zalando.com/skipper/), an HTTP router and reverse proxy for service composition

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/skipper0.18/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/skipper0.18/
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
unikraft build . --output <my-org>/skipper018:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000,stateful=true --metro fra -p 443:9090/tls+http -m 256M --image <my-org>/skipper018:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 443:9090/tls+http -M 256Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         skipper018-mx4ai
uuid:         34e3d740-c2b0-4644-b7e1-647350f688dc
state:        starting
image:        <my-org>/skipper018
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       b32c9035-d669-79fa-9955-9ad52cd1fcb4
  name:       aged-sea-o7d3c42s
  domains:
  - fqdn:     aged-sea-o7d3c42s.fra.unikraft.app
networks:
- uuid:       70cfb329-9ab3-fc8c-aff9-a3bbbbeb70f3
  private-ip: 10.0.6.4
  mac:        12:b0:32:1b:02:7b
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: skipper018-mx4ai
 ├───────── uuid: 34e3d740-c2b0-4644-b7e1-647350f688dc
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://aged-sea-o7d3c42s.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/skipper018@sha256:5483eaf3612cca2116ceaab9be42557686324f1d30337ae15d0495eef63d0386
 ├─────── memory: 256 MiB
 ├────── service: aged-sea-o7d3c42s
 ├─ private fqdn: skipper018-mx4ai.internal
 └─── private ip: 10.0.6.4
```

In this case, the instance name is `skipper018-mx4ai` and the address is `https://aged-sea-o7d3c42s.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Skipper.

```bash
curl https://aged-sea-o7d3c42s.fra.unikraft.app
```

```text
Hello, world from Skipper on Unikraft!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME              STATE    IMAGE                ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    skipper018-mx4ai  running  <my-org>/skipper018        256MiB  1      aged-sea-o7d3c42s.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME              FQDN                                STATE    STATUS        IMAGE                                             MEMORY   VCPUS  ARGS  BOOT TIME
skipper018-mx4ai  aged-sea-o7d3c42s.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/skipper018@sha256:...  256 MiB  1            43.71 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete skipper018-mx4ai
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove skipper018-mx4ai
```

## Customize your app

To customize Skipper you can change the `example.eskip` configuration file.

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
