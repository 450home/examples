# Minio

This guide shows you how to use [MinIO](https://min.io), a High Performance Object Storage which is
Open Source, Amazon S3 compatible, Kubernetes Native and works for cloud native workloads like AI.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/minio/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/minio/
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
unikraft build . --output <my-org>/minio:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:9001/tls+http -p 9000:9000/tls -m 512M --image <my-org>/minio:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:9001/tls+http -p 9000:9000/tls -M 512Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         minio-w2my8
uuid:         31e691ad-05a0-48b6-ad49-7f79da8e1754
state:        starting
image:        <my-org>/minio
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       8fdad5ff-9276-5f35-f94e-3d9d9b244a15
  name:       icy-bird-tregaga9
  domains:
  - fqdn:     icy-bird-tregaga9.fra.unikraft.app
networks:
- uuid:       f3a7d1f6-b1ca-68d0-6b45-7e9179ad0966
  private-ip: 10.0.6.4
  mac:        12:b0:44:5e:b0:54
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: minio-w2my8
 ├───────── uuid: 31e691ad-05a0-48b6-ad49-7f79da8e1754
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://icy-bird-tregaga9.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/minio@sha256:ba4657c607495326b0e29b512fb33a4179cd1b2a15fbfdd3ccc6e66209a701dd
 ├─────── memory: 512 MiB
 ├────── service: icy-bird-tregaga9
 ├─ private fqdn: minio-w2my8.internal
 └─── private ip: 10.0.6.4
```

In this case, the instance name is `minio-w2my8` and the address is `https://icy-bird-tregaga9.fra.unikraft.app`.
They're different for each run.

To test, point your browser at the address.
The default account/password are `minioadmin/minioadmin`.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME         STATE    IMAGE           ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    minio-w2my8  running  <my-org>/minio        512MiB  1      icy-bird-tregaga9.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME         FQDN                                STATE    STATUS        IMAGE                                        MEMORY   VCPUS  ARGS  BOOT TIME
minio-w2my8  icy-bird-tregaga9.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/minio@sha256:...  512 MiB  1            73.65 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete minio-w2my8
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove minio-w2my8
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
