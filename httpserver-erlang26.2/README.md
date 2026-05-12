# Erlang HTTP Server

This guide explains how to create and deploy a simple Erlang-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

> **Note**:
> The unikraft CLI is the current standard, while kraft is the legacy version.
> Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-erlang26.2/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/httpserver-erlang26.2/
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
unikraft build . --output <my-org>/httpserver-erlang262:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/httpserver-erlang262:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 512Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-erlang262-sw2bp
uuid:         1c4a8a51-fb61-45fc-87b8-26d192a7c2bc
state:        starting
image:        <my-org>/httpserver-erlang262
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       c7a6b443-c424-8a96-ce90-e833841b6eca
  name:       patient-field-ck629j2u
  domains:
  - fqdn:     patient-field-ck629j2u.fra.unikraft.app
networks:
- uuid:       6d767165-9196-e27d-bb12-5eb5a9188654
  private-ip: 10.0.3.3
  mac:        12:b0:05:ce:23:30
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-erlang262-sw2bp
 ├───────── uuid: 1c4a8a51-fb61-45fc-87b8-26d192a7c2bc
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://patient-field-ck629j2u.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-erlang262@sha256:d99feefa7973ba43f726356497f54c34a16421aa25a27fa547d2c1add418204e
 ├─────── memory: 512 MiB
 ├────── service: patient-field-ck629j2u
 ├─ private fqdn: httpserver-erlang262-sw2bp.internal
 └─── private ip: 10.0.3.3
```

In this case, the instance name is `httpserver-erlang262-sw2bp` and the address is `https://patient-field-ck629j2u.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Erlang-based HTTP web server:

```bash
curl https://patient-field-ck629j2u.fra.unikraft.app
```

```text
Hello, World!
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                        STATE    IMAGE                          ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    httpserver-erlang262-sw2bp  running  <my-org>/httpserver-erlang262        512MiB  1      patient-field-ck629j2u.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                        FQDN                                     STATE    STATUS        IMAGE                                                       MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-erlang262-sw2bp  patient-field-ck629j2u.fra.unikraft.app  running  since 35secs  oci://unikraft.io/<my-org>/httpserver-erlang262@sha256:...  512 MiB  1            404.04 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-erlang262-sw2bp
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-erlang262-sw2bp
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `http_server.erl`: the actual Erlang HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `http_server.erl` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

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
