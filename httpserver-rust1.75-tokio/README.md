# Rust (Tokio) HTTP Server

This example uses [`Tokio`](https://tokio.rs/), a popular Rust asynchronous runtime.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

1. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-rust1.75-tokio/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-rust1.75-tokio/
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
unikraft build . --output <my-org>/httpserver-rust175-tokio:latest
unikraft run --metro fra \
  -m 256M \
  -p 443:8080/tls+http \
  --scale-to-zero policy=on,cooldown-time=1000 \
  --image <my-org>/httpserver-rust175-tokio:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 256Mi \
  -p 443:8080/tls+http \
  --scale-to-zero on \
  --scale-to-zero-cooldown 1s \
  .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-rust175-tokio-6gxsp
uuid:         d5719f64-0653-42d7-b2de-aa6dee0ce467
state:        starting
image:        <my-org>/httpserver-rust175-tokio
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       b59ce5aa-7dac-5241-386c-be48db955f3f
  name:       empty-dawn-3coedrce
  domains:
  - fqdn:     empty-dawn-3coedrce.fra.unikraft.app
networks:
- uuid:       9136307f-2ee6-2a0b-99af-c5a0fc1727f5
  private-ip: 10.0.6.3
  mac:        12:b0:38:a0:73:f3
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-rust175-tokio-6gxsp
 ├───────── uuid: d5719f64-0653-42d7-b2de-aa6dee0ce467
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://empty-dawn-3coedrce.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-rust175-tokio@sha256:0ce75912711aa2329232a2ca6c3ccb7a244b6d546fafc081f815c2fde8224856
 ├─────── memory: 256 MiB
 ├────── service: empty-dawn-3coedrce
 ├─ private fqdn: httpserver-rust175-tokio-6gxsp.internal
 └─── private ip: 10.0.6.3
```

In this case, the instance name is `httpserver-rust175-tokio-6gxsp` and the address is `https://empty-dawn-3coedrce.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the Tokio-based HTTP web server:

```bash
curl https://empty-dawn-3coedrce.fra.unikraft.app
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
METRO  NAME                            STATE    IMAGE                              ARGS  MEMORY  VCPUS  FQDN                                  CREATED
fra    httpserver-rust175-tokio-6gxsp  running  <my-org>/httpserver-rust175-tokio        256MiB  1      empty-dawn-3coedrce.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                            FQDN                                  STATE    STATUS        IMAGE                                                           MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-rust175-tokio-6gxsp  empty-dawn-3coedrce.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-rust175-tokio@sha256:...  256 MiB  1            21.41 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-rust175-tokio-6gxsp
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-rust175-tokio-6gxsp
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.rs`: the actual server
* `Cargo.toml`: the Cargo package manager configuration file
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `src/main.rs` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.
  If you add new Rust source code files, be sure to configure required dependencies in the `Cargo.toml` file.

* If you build a new executable, update the `cmd` line in the `Kraftfile` and replace `/server` with the path to the new executable.

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
