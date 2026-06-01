# SSH and HTTP Server with C and Debugging Tools

This guide explains how to create and deploy a C app with debugging enabled.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-c-debug` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-c-debug/
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

For extensive debug information with `strace`, add the `USE_STRACE=1` environment variable to the deploy command:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/httpserver-c-debug:latest
unikraft run --scale-to-zero policy=off --metro fra -p 443:8080/tls+http -p 2222:2222/tls -e PUBKEY=.... -e USE_STRACE=1 -m 256M --image <my-org>/httpserver-c-debug:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero off -p 443:8080/tls+http -p 2222:2222/tls -M 256Mi -e PUBKEY="...." -e USE_STRACE=1 .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-c-debug-5pvem
uuid:         08629a94-e2b1-466e-abb9-15ce46411b66
state:        starting
image:        <my-org>/httpserver-c-debug
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       2e016406-0c59-4d74-6deb-fdcb206fdb1e
  name:       patient-snow-zdzhdy8r
  domains:
  - fqdn:     patient-snow-zdzhdy8r.fra.unikraft.app
networks:
- uuid:       80a11393-8eca-ec11-3028-fb8908b21894
  private-ip: 10.0.0.109
  mac:        12:b0:45:b3:18:b2
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-c-debug-5pvem
 ├───────── uuid: 08629a94-e2b1-466e-abb9-15ce46411b66
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://patient-snow-zdzhdy8r.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-c-debug@sha256:b24b95e236c8eff69615dd4f5d257beed5ee4047fd98d1b6fb200f89c63fa54c
 ├─────── memory: 256 MiB
 ├────── service: patient-snow-zdzhdy8r
 ├─ private fqdn: httpserver-c-debug-5pvem.internal
 └─── private ip: 10.0.0.109
```

In this case, the instance name is `httpserver-c-debug-5pvem` and the address is `patient-snow-zdzhdy8r.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance:

```bash
curl https://patient-snow-zdzhdy8r.fra.unikraft.app
```

```text
Hello, World!
```

For SSH, you need to set up a tunnel that handles the TLS connection to the Unikraft Cloud instance.
This way, you have a non-TLS port that your SSH client can connect to:

```bash
socat TCP-LISTEN:2222,reuseaddr,fork OPENSSL:patient-snow-zdzhdy8r.fra.unikraft.app:2222,verify=0
```

Then connect to the instance via SSH using:

```bash
ssh -l root localhost -p 2222
```

You might see warnings like `REMOTE HOST IDENTIFICATION HAS CHANGED`.
This is normal if you have set up tunnels to connect with SSH on `localhost`, so don't worry.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                      STATE    IMAGE                        ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    httpserver-c-debug-5pvem  running  <my-org>/httpserver-c-debug        256MiB  1      patient-snow-zdzhdy8r.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                      FQDN                                    STATE    STATUS       IMAGE                                                     MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-c-debug-5pvem  patient-snow-zdzhdy8r.fra.unikraft.app  running  since 4mins  oci://unikraft.io/<my-org>/httpserver-c-debug@sha256:...  256 MiB  1            66.56 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-c-debug-5pvem
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-c-debug-5pvem
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
