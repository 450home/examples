# Spring PetClinic

[Spring PetClinic](https://github.com/spring-projects/spring-petclinic) is an example project that uses Spring boot to model a simple pet clinic.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/httpserver-java17-spring-petclinic/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/httpserver-java17-spring-petclinic/
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
unikraft build . --output <my-org>/httpserver-java17-spring-petclinic:latest
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -p 443:8080/tls+http -m 1G --image <my-org>/httpserver-java17-spring-petclinic:latest
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s --metro fra -p 443:8080/tls+http -M 1Gi .
```

The output shows the instance address and other details:

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         httpserver-java17-spring-petclinic-r4s3x
uuid:         5a3b7e2c-1f4d-4a8e-b6c9-2d3f8a1e7b4c
state:        starting
image:        <my-org>/httpserver-java17-spring-petclinic
resources:
  memory:     1024MiB
  vcpus:      1
service:
  uuid:       f4c2b1a0-3e5d-8b7a-9c6d-1e2f3a4b5c6d
  name:       bitter-dust-a7b2c3d4
  domains:
  - fqdn:     bitter-dust-a7b2c3d4.fra.unikraft.app
networks:
- uuid:       7d6e5f4a-3b2c-1d0e-9f8a-7b6c5d4e3f2a
  private-ip: 10.0.4.2
  mac:        12:b0:4a:1c:8f:73
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: httpserver-java17-spring-petclinic-r4s3x
 ├───────── uuid: 5a3b7e2c-1f4d-4a8e-b6c9-2d3f8a1e7b4c
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://bitter-dust-a7b2c3d4.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/httpserver-java17-spring-petclinic@sha256:3e9d1f8a7b2c4e5f6a3b8c2d1e4f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f
 ├─────── memory: 1024 MiB
 ├────── service: bitter-dust-a7b2c3d4
 ├─ private fqdn: httpserver-java17-spring-petclinic-r4s3x.internal
 └─── private ip: 10.0.4.2
```

In this case, the instance name is `httpserver-java17-spring-petclinic-r4s3x` and the address is `https://bitter-dust-a7b2c3d4.fra.unikraft.app`.
They're different for each run.

After deploying, point your browser to the provided URL.

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

```ansi title="unikraft"
METRO  NAME                                      STATE    IMAGE                                        ARGS  MEMORY   VCPUS  FQDN                                   CREATED
fra    httpserver-java17-spring-petclinic-r4s3x  running  <my-org>/httpserver-java17-spring-petclinic        1024MiB  1      bitter-dust-a7b2c3d4.fra.unikraft.app  2 minutes ago
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

```ansi title="kraft"
NAME                                      FQDN                                   STATE    STATUS        IMAGE                                                                     MEMORY   VCPUS  ARGS  BOOT TIME
httpserver-java17-spring-petclinic-r4s3x  bitter-dust-a7b2c3d4.fra.unikraft.app  running  1 minute ago  oci://unikraft.io/<my-org>/httpserver-java17-spring-petclinic@sha256:...  1.0 GiB  1            521.43 ms
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete <instance-name>
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove <instance-name>
```


## Learn more

- [Spring Boot Reference](https://docs.spring.io/spring-boot/docs/current/reference/html/)
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
