# DuckDB with Go

This guide shows you how to use [DuckDB](https://duckdb.org), an in-process SQL OLAP database management system, in your Go project.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/duckdb-go1.21/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/duckdb-go1.21/
```

Make sure to log into Unikraft Cloud and pick a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash title="unikraft"
unikraft login
```

or

```bash title="kraft"
# Set Unikraft Cloud access token
export UKC_TOKEN=token
# Set metro to Frankfurt, DE
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash title="unikraft"
unikraft build . --output <my-org>/duckdb-go1.21:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000,stateful=true --metro fra -p 443:8080/tls+http -m 256M --image <my-org>/duckdb-go1.21:latest
```

or

```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 256Mi .
```

The output shows the instance address and other details:

```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: duckdb-go1.21-qfd8x
 ├───────── uuid: 90960d27-458b-4dd7-a037-2a9a3a47f095
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://autumn-gorilla-hg4h6sup.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/duckdb-go1.21@sha256:6999293f8694ac00beb6a1d639fab8f96f78c2e6ecb8ccb2311539908895a699
 ├─────── memory: 256 MiB
 ├────── service: autumn-gorilla-hg4h6sup
 ├─ private fqdn: duckdb-go1.21-qfd8x.internal
 └─── private ip: 10.0.6.2
```

or

```ansi title="unikraft"
metro:        fra
name:         duckdb-go1.21-qfd8x
uuid:         90960d27-458b-4dd7-a037-2a9a3a47f095
state:        starting
image:        <my-org>/duckdb-go1.21
resources:
  memory:     256MiB
  vcpus:      1
service:
  uuid:       0e3c61f1-5ad3-7d75-ceaf-079ea83394f6
  name:       autumn-gorilla-hg4h6sup
  domains:
  - fqdn:     autumn-gorilla-hg4h6sup.fra.unikraft.app
networks:
- uuid:       0f66c51a-dcad-94fc-d0a8-b0570e3d1b97
  private-ip: 10.0.6.2
  mac:        12:b0:31:d1:4b:90
timestamps:
  created:    just now
```

In this case, the instance name is `duckdb-go1.21-qfd8x` and the address is `https://autumn-gorilla-hg4h6sup.fra.unikraft.app`.
They're different for each run.

Use `curl` to query the Unikraft Cloud instance of DuckDB.

```bash
curl https://autumn-gorilla-hg4h6sup.fra.unikraft.app
```

```text
id: %d, name: %s 42 John
```

You can list information about the instance by running:

```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                 STATE    IMAGE                   ARGS  MEMORY  VCPUS  FQDN                                      CREATED
fra    duckdb-go1.21-qfd8x  running  <my-org>/duckdb-go1.21        256MiB  1      autumn-gorilla-hg4h6sup.fra.unikraft.app  2 minutes ago
```

or

```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                 FQDN                                      STATE    STATUS        IMAGE                                                MEMORY   VCPUS  ARGS  BOOT TIME
duckdb-go1.21-qfd8x  autumn-gorilla-hg4h6sup.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/duckdb-go1.21@sha256:...  256 MiB  1            32.12 ms
```

When done, you can remove the instance:

```bash title="unikraft"
unikraft instances delete duckdb-go1.21-qfd8x
```

or

```bash title="kraft"
kraft cloud instance remove duckdb-go1.21-qfd8x
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `src/main.go`: the Go web server frontend
* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: the Docker-specified app filesystem

The following options are available for customizing the app:

* If you only update the implementation in the `main.go` source file, you don't need to make any other changes.

* If you create any new source files, copy them into the app filesystem by using the `COPY` command in the `Dockerfile`.

* If you add new source code files, build them using the corresponding `go build` command.

* If you build a new executable, update the `cmd` line in the `Kraftfile` and replace `/server` with the path to the new executable.

* More extensive changes may require extending the `Dockerfile` ([see `Dockerfile` syntax reference](https://docs.docker.com/engine/reference/builder/)).

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash title="unikraft"
unikraft --help
```

or

```bash title="kraft"
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/unikraft) or the [legacy CLI Reference](https://unikraft.com/docs/cli/kraft/overview).
