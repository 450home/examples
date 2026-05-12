# Debian SSH server

This guide explains how to create and deploy a Debian app with SSH enabled.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/debian-ssh` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/debian-ssh/
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
unikraft build . --output <my-org>/debian-ssh:latest
unikraft run --scale-to-zero policy=off --metro fra -p 2222:2222/tls -m 1G -e PUBKEY="...." --image <my-org>/debian-ssh:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero off -p 2222:2222/tls -M 1Gi -e PUBKEY="...." .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         debian-ssh-2uwg5
uuid:         b3d158c5-fb52-4685-a76b-2497973308dc
state:        starting
image:        <my-org>/debian-ssh
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       5771bead-c045-52fa-1f89-5bc4f1cf3c38
  name:       nameless-cherry-sw2e9ul2
  domains:
  - fqdn:     nameless-cherry-sw2e9ul2.fra.unikraft.app
networks:
- uuid:       9d76ad3f-2149-f0af-d77f-76daba253d33
  private-ip: 10.0.0.109
  mac:        12:b0:1d:bd:54:f6
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: debian-ssh-2uwg5
 ├───────── uuid: b3d158c5-fb52-4685-a76b-2497973308dc
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://nameless-cherry-sw2e9ul2.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/debian-ssh@sha256:2442b4d5e078e7bc9ccd887fac65623511551592315d341a219f34a2c6628949
 ├─────── memory: 1024 MiB
 ├────── service: nameless-cherry-sw2e9ul2
 ├─ private fqdn: debian-ssh-2uwg5.internal
 └─── private ip: 10.0.0.109
```

In this case, the instance name is `debian-ssh-2uwg5` and the address is `nameless-cherry-sw2e9ul2.fra.unikraft.app`.
They're different for each run.

You need to set up a tunnel that handles the TLS connection to the Unikraft Cloud instance.
This way, you have a non-TLS port that your SSH client can connect to:

```bash
socat TCP-LISTEN:2222,reuseaddr,fork OPENSSL:nameless-cherry-sw2e9ul2.fra.unikraft.app:2222,verify=0
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
METRO  NAME              STATE    IMAGE                ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    debian-ssh-2uwg5  running  <my-org>/debian-ssh        1.0GiB  1      nameless-cherry-sw2e9ul2.fra.unikraft…  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME              FQDN                                       STATE    STATUS       IMAGE                                             MEMORY   VCPUS  ARGS  BOOT TIME
debian-ssh-2uwg5  nameless-cherry-sw2e9ul2.fra.unikraft.app  running  since 5mins  oci://unikraft.io/<my-org>/debian-ssh@sha256:...  1.0 GiB  1            217.26 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete debian-ssh-2uwg5
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove debian-ssh-2uwg5
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
