# Neo4j

This guide shows you how to use [Neo4j](https://neo4j.com), one of the most popular open source graph databases.
To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/neo4j/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/neo4j/
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
unikraft build . --output <my-org>/neo4j:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:7474/tls+http \
  -p 7687:7687/tls \
  --scale-to-zero policy=idle,cooldown-time=4000,stateful=true \
  -e "NEO4J_HOME=/var/lib/neo4j" \
  -e "JAVA_HOME=/opt/java/openjdk" \
  -e "LANG=C.UTF-8" \
  -e "NEO4J_EDITION=community" \
  -e "PATH=/var/lib/neo4j/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
  --image <my-org>/neo4j:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 2Gi \
  -p 443:7474/tls+http \
  -p 7687:7687/tls \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 4s \
  --env NEO4J_HOME=/var/lib/neo4j \
  --env JAVA_HOME=/opt/java/openjdk \
  --env LANG=C.UTF-8 \
  --env NEO4J_EDITION=community \
  --env PATH=/var/lib/neo4j/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  .
```

> **Note**:
> You can also set a custom password for the default neo4j user by adding the
> following env var to the run command
> `-e "NEO4J_AUTH_PASSWORD=..."`

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:           fra
name:            neo4j-t117i
uuid:            c59f865e-e954-4bf8-8da8-7ee6f1c1aab2
state:           starting
image:           <my-org>/neo4j
resources:
  memory:        2GiB
  vcpus:         1
service:
  name:          fragrant-fog-pj1gi4jl
  uuid:          a3d29dfa-650b-4e8c-a8e6-055f59dd4c92
  domains:
  - fqdn:        fragrant-fog-pj1gi4jl.fra.unikraft.app
networks:
- uuid:          1a65f2c3-cbfd-48bf-b8db-5cb90ed62a7c
  private-ip:    10.0.1.73
  mac:           12:b0:0a:00:01:49
timestamps:
  created:       just now
scale-to-zero:
  enabled:       true
  policy:        idle
  stateful:      true
  cooldown-time: 4s
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: neo4j-t117i
 ├───────── uuid: c59f865e-e954-4bf8-8da8-7ee6f1c1aab2
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://fragrant-fog-pj1gi4jl.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/neo4j@sha256:2476c0373d663d7604def7c35ffcb4ed4de8ab231309b4f20104b84f31570766
 ├─────── memory: 2048 MiB
 ├────── service: fragrant-fog-pj1gi4jl
 ├─ private fqdn: neo4j-t117i.internal
 └─── private ip: 10.0.1.73
```

In this case, the instance name is `neo4j-t117i` and the address is `https://fragrant-fog-pj1gi4jl.fra.unikraft.app`
They're different for each run.

Use `curl` to query the Unikraft Cloud Neo4j instance:

```bash
curl https://fragrant-fog-pj1gi4jl.fra.unikraft.app
```

```text
{"bolt_routing":"neo4j://fragrant-fog-pj1gi4jl.fra.unikraft.app:7687","query":"https://fragrant-fog-pj1gi4jl.fra.unikraft.app:7687/db/{databaseName}/query/v2","transaction":"https://fragrant-fog-pj1gi4jl.fra.unikraft.app/db/{databaseName}/tx","bolt_direct":"bolt://fragrant-fog-pj1gi4jl.fra.unikraft.app:7687","neo4j_version":"2026.04.0","neo4j_edition":"community"}
```

Or even better, point a browser at it 😀. Make sure you have the protocol set
to `neo4j+s` when logging in.

You can also try connecting to the instance using the `cypher-shell` CLI
```bash
cypher-shell -a neo4j+s://fragrant-fog-pj1gi4jl.fra.unikraft.app:7687 -u neo4j
```

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME            STATE    IMAGE              ARGS  MEMORY  VCPUS  FQDN                                     CREATED
fra    neo4j-t117i     standby  <my-org>/neo4j          2GiB    1      fragrant-fog-pj1gi4jl.fra.unikraft.app   just now
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME            FQDN                                     STATE    STATUS         IMAGE                                           MEMORY   VCPUS  ARGS  BOOT TIME
neo4j-t117i     fragrant-fog-pj1gi4jl.fra.unikraft.app  standby  2 minutes ago  oci://unikraft.io/<my-org>/neo4j@sha256:...  2.0 GiB  1            603.42 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete neo4j-t117i
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove neo4j-t117i
```

## Using volumes

You can use [volumes](https://unikraft.com/docs/platform/volumes) for data persistence for your neo4j instance.
For that you would first create a volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --set metro=fra --set name=neo4j-store --set size=512M
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name neo4j-store --size 512Mi
```

Then start the neo4j instance and mount that volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/neo4j:latest
unikraft run --metro fra \
  -m 2G \
  -p 443:7474/tls+http \
  -p 7687:7687/tls \
  --scale-to-zero policy=idle,cooldown-time=4000,stateful=true \
  -e "NEO4J_HOME=/var/lib/neo4j" \
  -e "JAVA_HOME=/opt/java/openjdk" \
  -e "LANG=C.UTF-8" \
  -e "NEO4J_EDITION=community" \
  -e "PATH=/var/lib/neo4j/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
  --volume neo4j-store:/data \
  --image <my-org>/neo4j:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy \
  -M 2Gi \
  -p 443:7474/tls+http \
  -p 7687:7687/tls \
  --scale-to-zero idle \
  --scale-to-zero-stateful \
  --scale-to-zero-cooldown 4s \
  --env NEO4J_HOME=/var/lib/neo4j \
  --env JAVA_HOME=/opt/java/openjdk \
  --env LANG=C.UTF-8 \
  --env NEO4J_EDITION=community \
  --env PATH=/var/lib/neo4j/bin:/opt/java/openjdk/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  --volume neo4j-store:/data \
  .
```

## Customize your app

To customize the app, update the files in the repository, listed below:

* `Kraftfile`: the Unikraft Cloud specification, including command-line arguments
* `Dockerfile`: In case you need to add files to your instance's rootfs

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
