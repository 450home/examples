# Phoenix with PostgreSQL

[Phoenix](https://phoenixframework.org/) is a web development framework written in Elixir, designed for building scalable and maintainable applications. This example demonstrates how to deploy a Phoenix application with a PostgreSQL database on [Unikraft Cloud](https://unikraft.cloud/).

This example app has been generated using [Phoenix Express](https://hexdocs.pm/phoenix/up_and_running.html#phoenix-express), and the Dockerfile
used for building the rootfs was generated following the instructions [here](https://hexdocs.pm/phoenix/releases.html).

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/phoenix-postgres` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/phoenix-postgres/
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

Create a volume for PostgreSQL data persistence:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --metro fra --name db-data --size 512M
```

```ansi title="unikraft"
metro:        fra
name:         db-data
uuid:         0efda5f6-21d2-48c7-84f5-8efe87e33090
state:        available
size:         512MiB
filesystem:   ext4
quota-policy: static
persistent:   true
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name db-data --size 512
```

```ansi title="kraft"
[+] Created volume 'db-data' (512 MiB)
```

## Build and deploy the PostgreSQL instance.

Update `POSTGRES_PASSWORD` with a secure password:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./postgres --output <my-org>/postgres:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -m 2G --volume db-data:/var/lib/postgresql/data --image <my-org>/postgres:latest --domain postgres.internal --env POSTGRES_USER=postgres --env POSTGRES_PASSWORD=example_123 --env POSTGRES_DB=myapp_prod --env PGDATA=/var/lib/postgresql/data/pgdata
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -M 2Gi --volume db-data:/var/lib/postgresql/data --domain postgres.internal --env POSTGRES_USER=postgres --env POSTGRES_PASSWORD=example_123 --env POSTGRES_DB=myapp_prod --env PGDATA=/var/lib/postgresql/data/pgdata postgres/
```

Make sure to replace `<my-org>` with your username / org-name.

The output shows the PostgreSQL instance details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:                 fra
name:                  postgres-ik5at
uuid:                  3776dbfe-2937-45e7-8079-c54275ef3cff
state:                 starting
image:                 <my-org>/postgres
runtime:
  env:
    PGDATA:            /var/lib/postgresql/data/pgdata
    POSTGRES_DB:       myapp_prod
    POSTGRES_PASSWORD: *
    POSTGRES_USER:     postgres
resources:
  memory:              2GiB
  vcpus:               1
service:
  name:                dry-cloud-q8u7yjkl
  uuid:                cf364e60-46b0-4031-bace-296fa8e24ac4
  domains:
  - fqdn:              postgres.internal
volumes:
- name:                db-data
  uuid:                0efda5f6-21d2-48c7-84f5-8efe87e33090
  at:                  /var/lib/postgresql/data
networks:
- uuid:                cab79d9f-08a8-4741-8efd-58d9a1faa35d
  private-ip:          10.0.14.117
  mac:                 12:b0:0a:00:0e:75
timestamps:
  created:             just now
scale-to-zero:
  enabled:             true
  policy:              idle
  stateful:            true
  cooldown-time:       1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: postgres-ik5at
 ├───────── uuid: 3776dbfe-2937-45e7-8079-c54275ef3cff
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: postgres.internal
 ├──────── image: oci://unikraft.io/<my-org>/postgres@sha256:...
 ├─────── memory: 2048 MiB
 ├────── service: dry-cloud-q8u7yjkl
 ├─ private fqdn: postgres-ik5at.internal
 └─── private ip: 10.0.14.117
```

## Build and deploy the Phoenix instance.

Generate a secret key for Phoenix:

```bash
openssl rand -base64 48
```

Replace `<your-secret-key-base>` in the commands below with the generated value, and update the password in `DATABASE_URL` to match the one set for PostgreSQL:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build ./phoenix --output <my-org>/phoenix:latest
unikraft run --scale-to-zero policy=on,cooldown-time=1000 --metro fra -p 443:4000/tls+http -m 2G --image <my-org>/phoenix:latest --env SECRET_KEY_BASE=<your-secret-key-base> --env DATABASE_URL=ecto://postgres:example_123@postgres.internal:5432/myapp_prod
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero on --scale-to-zero-cooldown 1s -p 443:4000/tls+http -M 2Gi --env SECRET_KEY_BASE=<your-secret-key-base> --env DATABASE_URL=ecto://postgres:example_123@postgres.internal:5432/myapp_prod phoenix/
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:               fra
name:                phoenix-hd29m
uuid:                fa4db9cf-f7b5-4b8b-b007-8fd1ce87c7e1
state:               starting
image:               <my-org>/phoenix
runtime:
  env:
    DATABASE_URL:    ecto://postgres:example_123@postgres.internal:5432/myapp_prod
    SECRET_KEY_BASE: <your-secret-key-base>
resources:
  memory:            2GiB
  vcpus:             1
service:
  name:              wild-moon-pkwsqc49
  uuid:              1d1b8732-d2d5-41ab-ab8f-1b19fc27c14d
  domains:
  - fqdn:            wild-moon-pkwsqc49.fra.unikraft.app
networks:
- uuid:              d14f07de-1c81-4309-bbf3-ab8ab6aeefe6
  private-ip:        10.0.14.53
  mac:               12:b0:0a:00:0e:35
timestamps:
  created:           just now
scale-to-zero:
  enabled:           true
  policy:            on
  cooldown-time:     1s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: phoenix-hd29m
 ├───────── uuid: fa4db9cf-f7b5-4b8b-b007-8fd1ce87c7e1
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://wild-moon-pkwsqc49.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/phoenix@sha256:...
 ├─────── memory: 2048 MiB
 ├────── service: wild-moon-pkwsqc49
 ├─ private fqdn: phoenix-hd29m.internal
 └─── private ip: 10.0.14.53
```

In this case, the instance names are `postgres-ik5at` and `phoenix-hd29m`.
They're different for each run.

Use a browser to access the Phoenix application using the URL from the `fqdn` field in the output.

You can list information about the instances by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME             STATE   IMAGE              MEMORY  VCPUS  FQDN                                      CREATED
fra    phoenix-hd29m    running <my-org>/phoenix   2GiB    1      wild-moon-pkwsqc49.fra.unikraft.app       just now
fra    postgres-ik5at   standby <my-org>/postgres  2GiB    1      postgres.internal                         3 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME             FQDN                                        STATE    STATUS      IMAGE                                              MEMORY    VCPUS  ARGS  BOOT TIME
phoenix-hd29m    wild-moon-pkwsqc49.fra.unikraft.app         running  since now   oci://unikraft.io/<my-org>/phoenix@sha256:...      2048 MiB  1            158.32 ms
postgres-ik5at   postgres.internal                           standby  since 3min  oci://unikraft.io/<my-org>/postgres@sha256:...     2048 MiB  1            1811.99 ms
```

When done, you can remove the instances:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete postgres-ik5at phoenix-hd29m
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove postgres-ik5at phoenix-hd29m
```

## Volume

This deployment creates a volume (`db-data`) for PostgreSQL data persistence.
The volume persists after removing instances, allowing you to redeploy without losing data.
To remove the volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume delete db-data
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume remove db-data
```

## Learn more

- [Phoenix's Documentation](https://hexdocs.pm/phoenix/)
- [PostgreSQL's Documentation](https://www.postgresql.org/docs/)
- [Unikraft Cloud's Documentation](https://unikraft.cloud/docs/)
- [Building `Dockerfile` Images with `Buildkit`](https://unikraft.org/guides/building-dockerfile-images-with-buildkit)

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
