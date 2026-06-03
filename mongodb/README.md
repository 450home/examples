# MongoDB

This guide shows you how to use [MongoDB](https://www.mongodb.com), a source-available, cross-platform, document-oriented database program.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/mongodb/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/mongodb/
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
unikraft build . --output <my-org>/mongodb:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -p 27017:27017/tls -m 1G --image <my-org>/mongodb:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 27017:27017/tls -M 1Gi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         mongodb-6tiuu
uuid:         99779597-0bdb-4160-b902-a160c3ab4b2a
state:        starting
image:        <my-org>/mongodb
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       91309c0c-fd6f-271d-cab6-2694b0991fbe
  name:       bold-brook-khkwv7of
  domains:
  - fqdn:     bold-brook-khkwv7of.fra.unikraft.app
networks:
- uuid:       24cc79e5-bb3f-cdcd-fd5d-e4605015a228
  private-ip: 10.0.6.4
  mac:        12:b0:d7:7b:83:97
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: mongodb-6tiuu
 ├───────── uuid: 99779597-0bdb-4160-b902-a160c3ab4b2a
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://bold-brook-khkwv7of.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/mongodb@sha256:e6ff5153f106e2d5e2a10881818cd1b90fe3ff1294ad80879b2239ffc52aff0e
 ├─────── memory: 1024 MiB
 ├────── service: bold-brook-khkwv7of
 ├─ private fqdn: mongodb-6tiuu.internal
 └─── private ip: 10.0.6.4
```

In this case, the instance name is `mongodb-6tiuu` and the the address is
`bold-brook-khkwv7of.fra.unikraft.app` which is different for each run.

You can use the mongosh client to connect to the server:
```console
mongosh "mongodb://bold-brook-khkwv7of.fra.unikraft.app:27017/?tls=true"
```

You should see output like:

```console
Current Mongosh Log ID:	69d7a077dc5d28998344ba88
Connecting to:		mongodb://bold-brook-khkwv7of.fra.unikraft.app:27017/?tls=true&directConnection=true&appName=mongosh+2.8.2
Using MongoDB:		6.0.13
Using Mongosh:		2.8.2

For mongosh info see: https://docs.mongodb.com/mongodb-shell/

To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

test>
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME           STATE    IMAGE             ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    mongodb-6tiuu  running  <my-org>/mongodb        1.0GiB  1      bold-brook-khkwv7of.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME           FQDN                                  STATE    STATUS          IMAGE                                          MEMORY   VCPUS  ARGS  BOOT TIME
mongodb-6tiuu  bold-brook-khkwv7of.fra.unikraft.app  running  20 minutes ago  oci://unikraft.io/<my-org>/mongodb@sha256:...  1.0 GiB  1            82.41 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete mongodb-6tiuu
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove mongodb-6tiuu
```

## Using volumes

You can use [volumes](https://unikraft.com/docs/platform/volumes) for data persistence for your MongoDB instance.
For that you would first create a volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --set metro=fra --set name=mongodb-store --set size=512M
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name mongodb-store --size 512Mi
```

Then start the MongoDB instance and mount that volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/mongodb:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -p 27017:27017/tls -m 1G --volume mongodb-store:/data/db --image <my-org>/mongodb:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -M 1Gi -p 27017:27017/tls --volume mongodb-store:/data/db .
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
