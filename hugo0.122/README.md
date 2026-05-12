# Hugo

This guide shows you how to use [Hugo](https://gohugo.io/commands/hugo_server/), a high performance webserver, with the [ananke](https://github.com/budparr/gohugo-theme-ananke.git) theme.

To run it, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/hugo0.122/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/hugo0.122/
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
unikraft build . --output <my-org>/hugo0122:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:1313/tls+http -m 512M --image <my-org>/hugo0122:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:1313/tls+http -M 512Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         hugo0122-zpabu
uuid:         dfc6e06c-76cc-4aa1-a053-c4eded0d2456
state:        starting
image:        <my-org>/hugo0122
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       f5492054-269e-2bcb-1d6c-18b2129c423a
  name:       morning-rain-jikpfy3t
  domains:
  - fqdn:     morning-rain-jikpfy3t.fra.unikraft.app
networks:
- uuid:       4dd794e8-ee05-6d97-fdc8-b86f92dc1b44
  private-ip: 10.0.6.4
  mac:        12:b0:fe:77:90:47
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: hugo0122-zpabu
 ├───────── uuid: dfc6e06c-76cc-4aa1-a053-c4eded0d2456
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://morning-rain-jikpfy3t.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/hugo0122@sha256:68d20fdb707076b1cd0f2848b17cc75670d8a92b740edb9417aeb8463fef7f19
 ├─────── memory: 512 MiB
 ├────── service: morning-rain-jikpfy3t
 ├─ private fqdn: hugo0122-zpabu.internal
 └─── private ip: 10.0.6.4
```

In this case, the instance name is `hugo0122-zpabu` and the address is `https://morning-rain-jikpfy3t.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of Hugo.

```bash
curl https://morning-rain-jikpfy3t.fra.unikraft.app
```

```html
<!DOCTYPE html>
<html lang="en-us">
  <head><script src="/livereload.js?mindelay=10&amp;v=2&amp;port=1313&amp;path=livereload" data-no-instant defer></script>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
[...]
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME            STATE    IMAGE              ARGS  MEMORY  VCPUS  FQDN                                    CREATED
fra    hugo0122-zpabu  running  <my-org>/hugo0122        512MiB  1      morning-rain-jikpfy3t.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME            FQDN                                    STATE    STATUS        IMAGE                                           MEMORY   VCPUS  ARGS  BOOT TIME
hugo0122-zpabu  morning-rain-jikpfy3t.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/hugo0122@sha256:...  512 MiB  1            77.17 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete hugo0122-zpabu
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove hugo0122-zpabu
```

## Customize your app

To customize the Hugo app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification
* `site/`: sample site content
* `Dockerfile`: In case you need to add files to your instance's rootfs

Update the contents of the `site/` directory to serve different static web content.

After re-deploying the Hugo image on Unikraft Cloud, using `curl` or a browser to query it will present the new page contents.

Tools like [`Jekyll`](https://jekyllrb.com/) or [`Hugo`](https://gohugo.io/) can generate the static web content located in the `site/` offline.

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
