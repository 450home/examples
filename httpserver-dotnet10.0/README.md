# .NET HTTP Server

This guide explains how to create and deploy a simple .NET-based HTTP web server.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-dotnet10.0/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-dotnet10.0/
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
unikraft build . --output <my-org>/httpserver-dotnet100:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000,stateful=true --metro fra -p 443:8080/tls+http -m 512M --image <my-org>/httpserver-dotnet100:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 512Mi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-dotnet100-dsmkh
uuid:         25459494-cb43-4009-9d05-f0996de5b7e4
state:        starting
image:        <my-org>/httpserver-dotnet100
resources:
  memory:     512MiB
  vcpus:      1
service:
  uuid:       35a84131-01b7-b3cd-03a4-7acdd2c4f5f9
  name:       cold-fog-hl98aw6q
  domains:
  - fqdn:     cold-fog-hl98aw6q.fra.unikraft.app
networks:
- uuid:       d4ddf6b4-91e5-8692-03a2-1e42552f6dbe
  private-ip: 10.0.3.1
  mac:        12:b0:c0:f1:05:bd
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-dotnet100-dsmkh
 ├───────── uuid: 25459494-cb43-4009-9d05-f0996de5b7e4
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://cold-fog-hl98aw6q.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-dotnet100@sha256:4fad7453995ae96b636696e9929ee0e7376bfbbd63ab9698c1f1e02602aa2575
 ├─────── memory: 512 MiB
 ├────── service: cold-fog-hl98aw6q
 ├─ private fqdn: httpserver-dotnet100-dsmkh.internal
 └─── private ip: 10.0.3.1
```

In this case, the instance name is `httpserver-dotnet100-dsmkh` and the address is `https://cold-fog-hl98aw6q.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of the .NET-based HTTP web server:

```bash
curl https://cold-fog-hl98aw6q.fra.unikraft.app
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
METRO  NAME                        STATE    IMAGE                          ARGS  MEMORY  VCPUS  FQDN                                CREATED
fra    httpserver-dotnet100-dsmkh  running  <my-org>/httpserver-dotnet100        512MiB  1      cold-fog-hl98aw6q.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                        FQDN                                STATE    STATUS         IMAGE                                                       MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-dotnet100-dsmkh  cold-fog-hl98aw6q.fra.unikraft.app  running  2 minutes ago  oci://unikraft.io/<my-org>/httpserver-dotnet100@sha256:...  512 MiB  1            328.69 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete httpserver-dotnet100-dsmkh
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove httpserver-dotnet100-dsmkh
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `SimpleHttpServer.cs`: the actual .NET HTTP server implementation
* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile`: the Docker-specified app filesystem

Lines in the `Kraftfile` have the following roles:

* `spec: v0.7`: The current `Kraftfile` specification version is `0.7`.

* `runtime: base-compat:latest`: The runtime kernel to use is the base compatibility kernel.

* `rootfs`: Build the app root filesystem.
  `source: ./Dockerfile` means the filesystem is built using the `Dockerfile`.
  `format: erofs` means the filesystem type is [EROFS](https://erofs.docs.kernel.org/).

* `cmd:`: Use as the starting command of the instance.

Lines in the `Dockerfile` have the following roles:

* `WORKDIR /src`: Use the `/src` directory as the working directory.

* `RUN dotnet new console`: Create a new `dotnet` project.

* `RUN rm Program.cs`: Remove template source code file.

* `COPY ./SimpleHttpServer.cs .`: Copy the source code of the HTTP server.

* `RUN dotnet build .`: Build dotnet project.

* `FROM scratch`: Build the filesystem from the [`scratch` container image](https://hub.docker.com/_/scratch/), to [create a base image](https://docs.docker.com/build/building/base-images/).

* `COPY --from=build ...`: Copy on the required files from the filesystem: the binary executable, the .NET framework files and the binary library files.

The following options are available for customizing the app:

* If you only update the implementation in the `SimpleHttpServer.cs` source file, you don't need to make any other changes.

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
