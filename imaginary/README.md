# Imaginary

This example uses [`imaginary`](https://github.com/h2non/imaginary), an HTTP microservice for high-level image processing.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/imaginary/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/imaginary/
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
unikraft build . --output <my-org>/imaginary:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/imaginary:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 512Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         imaginary-mwb4y
uuid:         8cf18bf7-2bf6-4f23-be07-f9c234c7962d
state:        starting
image:        <my-org>/imaginary
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       b9b7fa60-5f4f-13e5-41e9-eeea476f4398
  name:       divine-wind-1ycjvhqs
  domains:
  - fqdn:     divine-wind-1ycjvhqs.fra.unikraft.app
networks:
- uuid:       91467bd9-8d52-a378-4426-7014ca09e5d5
  private-ip: 10.0.3.3
  mac:        12:b0:e2:ed:95:49
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: imaginary-mwb4y
 ├───────── uuid: 8cf18bf7-2bf6-4f23-be07-f9c234c7962d
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://divine-wind-1ycjvhqs.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/imaginary@sha256:673834bc531038bb621266f7fd635a04e559050cbe82876df811fd4b975ea4fe
 ├─────── memory: 512 MiB
 ├────── service: divine-wind-1ycjvhqs
 ├─ private fqdn: imaginary-mwb4y.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `imaginary-mwb4y` and the address is `https://divine-wind-1ycjvhqs.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Imaginary.
You will get a health status of the service:

```bash
curl -s https://divine-wind-1ycjvhqs.fra.unikraft.app/health | jq
```

```json
{
  "uptime": 414,
  "allocatedMemory": 0.19,
  "totalAllocatedMemory": 0.72,
  "goroutines": 6,
  "completedGCCycles": 13,
  "cpus": 1,
  "maxHeapUsage": 3.63,
  "heapInUse": 0.19,
  "objectsInUse": 846,
  "OSMemoryObtained": 7.73
}
```

To test the Imaginary instance on Unikraft Cloud use the `/form` endpoint.
That is, open the `https://divine-wind-1ycjvhqs.fra.unikraft.app/form` address in the browser and use the existing forms to process an image.

To make actual use of the Imaginary instance, use [the endpoints of the HTTP API](https://github.com/h2non/imaginary/blob/master/README.md#get).
The API provides endpoints, together with parameters, for different image processing options: `/crop`, `/resize`, `/flip`, `/convert`, `/watermark`, `/rotate`, `/blur` etc.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME             STATE    IMAGE               ARGS  MEMORY  VCPUS  FQDN                                   CREATED
fra    imaginary-mwb4y  running  <my-org>/imaginary        512MiB  1      divine-wind-1ycjvhqs.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME             FQDN                                   STATE    STATUS          IMAGE                                            MEMORY   VCPUS  ARGS  BOOT TIME
imaginary-mwb4y  divine-wind-1ycjvhqs.fra.unikraft.app  running  54 seconds ago  oci://unikraft.io/<my-org>/imaginary@sha256:...  512 MiB  1            32.26 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete imaginary-mwb4y
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove imaginary-mwb4y
```

The Imaginary Unikraft Cloud service works as is: you deploy it and then you query [the endpoints of the HTTP API](https://github.com/h2non/imaginary/blob/master/README.md#get).
You can customize the command line options used to start the service, by updating the `cmd` line in the `Kraftfile`:

```yaml
spec: v0.7

runtime: base-compat:latest

cmd: ["/usr/bin/imaginary", "-p", "8080"]
```

You can update the `cmd` line with [command line option for Imaginary](https://github.com/h2non/imaginary/blob/master/README.md#command-line-usage).

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
