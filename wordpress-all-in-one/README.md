# Wordpress

This guide shows you how to use [Wordpress](https://wordpress.com/), a web content management system.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.


2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/wordpress-all-in-one/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/wordpress-all-in-one/
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
unikraft build . --output <my-org>/wordpress-all-in-one:latest
unikraft run --scale-to-zero policy=on,cooldown-time=3000,stateful=true --metro fra -p 443:3000/tls+http -m 4G --image <my-org>/wordpress-all-in-one:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-stateful --scale-to-zero-cooldown 3s -p 443:3000/tls+http -M 4Gi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         wordpress-fx5rb
uuid:         bfb9d151-1604-452a-b2e0-f737486744df
state:        starting
image:        <my-org>/wordpress
resources:
  memory:     4096MiB
  vcpus:      1
service:
  uuid:       398fe5bb-e172-465e-8f74-56ffcfb24a3d
  name:       cool-silence-h5c1es4z
  domains:
  - fqdn:     cool-silence-h5c1es4z.fra.unikraft.app
networks:
- uuid:       26c200e0-43eb-dd46-e4be-e9505ff677d1
  private-ip: 10.0.3.1
  mac:        12:b0:4e:20:b3:e7
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: wordpress-fx5rb
 ├───────── uuid: bfb9d151-1604-452a-b2e0-f737486744df
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://cool-silence-h5c1es4z.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/wordpress@sha256:3e116e6c74dd04e19d4062a14f8173974ba625179ace3c10a2c96546638c4cd8
 ├─────── memory: 4096 MiB
 ├────── service: cool-silence-h5c1es4z
 ├─ private fqdn: wordpress-fx5rb.internal
 └─── private ip: 10.0.3.1
```

In this case, the instance name is `wordpress-fx5rb`.
They're different for each run.

Use a browser to access the install page of Wordpress.
Fill out the form and complete the Wordpress install.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME             STATE    IMAGE                          ARGS  MEMORY   VCPUS  FQDN                                    CREATED
fra    wordpress-fx5rb  running  <my-org>/wordpress-all-in-one        4096MiB  1      cool-silence-h5c1es4z.fra.unikraft.app  1 minute ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME             FQDN                                    STATE    STATUS        IMAGE                                                       MEMORY    VCPUS  ARGS  BOOT TIME
wordpress-fx5rb  cool-silence-h5c1es4z.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/wordpress-all-in-one@sha256:...  4096 MiB  1            245.32 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete wordpress-fx5rb
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove wordpress-fx5rb
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
