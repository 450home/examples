# vsftpd

This guide explains how to create and deploy a [vsftpd](https://security.appspot.com/vsftpd.html) app, to secure access to the files of your VM.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/vsftpd` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/vsftpd/
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
unikraft volume create --set metro=fra --set name=vsftpd-workspace --set size=1G

unikraft build . --output <my-org>/vsftpd:latest
unikraft run --metro fra --scale-to-zero policy=on,cooldown-time=40000,stateful=true -p 20:20/tls -p 21:21/tls -p 222:22/tls -p 990:990/tls -p 10100:10100/tls -m 1G --volume vsftpd-workspace:/root --image <my-org>/vsftpd:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name vsftpd-workspace --size 1Gi

kraft cloud deploy --scale-to-zero on --scale-to-zero-stateful --scale-to-zero-cooldown 3s --name vsftpd -p 20:20/tls -p 21:21/tls -p 222:22/tls -p 990:990/tls -p 10100:10100/tls -M 1Gi -v vsftpd-workspace:/root .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         vsftpd
uuid:         186a46a0-7c89-4bfd-83a8-649bcc60a96e
state:        starting
image:        <my-org>/vsftpd
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       4814b43a-c1d3-48f0-ef3e-9dba8bcaba25
  name:       broken-orangutan-jypu2z53
  domains:
  - fqdn:     broken-orangutan-jypu2z53.fra.unikraft.app
networks:
- uuid:       6adc6c29-5c9b-e472-70ff-fc3f3816d5a2
  private-ip: 10.0.0.109
  mac:        12:b0:17:ff:e4:c7
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: vsftpd
 ├───────── uuid: 186a46a0-7c89-4bfd-83a8-649bcc60a96e
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://broken-orangutan-jypu2z53.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/vsftpd@sha256:31aad1619c31f499b11f1bef8fead6e6df76f235a57add011e5e414a3f51ee64
 ├─────── memory: 1024 MiB
 ├────── service: broken-orangutan-jypu2z53
 ├─ private fqdn: vsftpd.internal
 └─── private ip: 10.0.0.109
```

This will create a volume for data persistence, and mount it at `/root` inside the VM.

In this case, the instance name is `vsftpd` and the address is `https://broken-orangutan-jypu2z53.fra.unikraft.app`.
The name was preset, but the address is different for each run.

**Note**: The `root` password defaults to `rootpass`.
Don't forget to change it inside the `Dockerfile` and update the commands below.

You can access the FTP server using a client like `lftp`:

```bash
lftp -u root,rootpass ftps://broken-orangutan-jypu2z53.fra.unikraft.app:21
lftp root@broken-orangutan-jypu2z53.fra.unikraft.app:~> ls
```

You can list information about the volume by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volumes list
```

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
METRO  NAME              STATE    SIZE    CREATED
fra    vsftpd-workspace  mounted  1.0GiB  9 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume list
```

**Using the legacy kraft CLI**
```ansi title="kraft"
NAME              CREATED AT     SIZE     ATTACHED TO  MOUNTED BY  STATE    PERSISTENT
vsftpd-workspace  9 minutes ago  1.0 GiB  vsftpd       vsftpd      mounted  true
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME    STATE    IMAGE            ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    vsftpd  standby  <my-org>/vsftpd        1.0GiB  1      broken-orangutan-jypu2z53.fra.unikraf…  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME    FQDN                                        STATE    STATUS   IMAGE                                         MEMORY   VCPUS  ARGS  BOOT TIME
vsftpd  broken-orangutan-jypu2z53.fra.unikraft.app  standby  standby  oci://unikraft.io/<my-org>/vsftpd@sha256:...  1.0 GiB  1            7.19 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete vsftpd
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove vsftpd
```

The volume isn't removed by default, so you can recreate the instance and still have access to your old data.
Remove it using:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume delete vsftpd-workspace
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume remove vsftpd-workspace
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
