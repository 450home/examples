# Chromium CDP with Token Authentication

This example uses Chromium, a headless browser exposing a [CDP (Chrome DevTools Protocol)](https://chromedevtools.github.io/devtools-protocol/) websocket interface, with token-based authentication and persistent storage.

## Features

- **Token authentication**: All CDP requests (HTTP and WebSocket) require a valid token
- **Admin API**: Create, list, and revoke tokens via REST endpoints
- **Bootstrap token**: Set an initial admin token via environment variable
- **Persistent storage**: The token database is stored on a volume that survives restarts

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

   > **Note**:
   > The unikraft CLI is the current standard, while kraft is the legacy version.
   > Choose one of the CLIs below and only run the commands associated with it for the rest of this guide.

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/chromium-cdp-auth/` directory:

   ```bash
   git clone https://github.com/unikraft-cloud/examples
   cd examples/chromium-cdp-auth/
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
export UKC_METRO=fra
```

The `UKC_TOKEN` and `UKC_METRO` environment variables are only supported by the legacy CLI.

Pick a bootstrap admin token that will be used for initial setup.
You pass it to the instance as the `BOOTSTRAP_ADMIN_TOKEN` environment variable (see the deploy commands below) and use it to create additional tokens:

```bash
export BOOTSTRAP_ADMIN_TOKEN=my-secret-admin-token
```

The token database is persisted on a [volume](https://unikraft.com/docs/platform/volumes) mounted at `/app/data`, so it survives restarts.
First create the volume:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft volume create --set metro=fra --set name=chromium-cdp-auth-data --set size=64M
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud volume create --name chromium-cdp-auth-data --size 64Mi
```

When done, invoke the following command to deploy this app on Unikraft Cloud, mounting the volume and passing the bootstrap token:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft build . --output <my-org>/chromium-cdp-auth
unikraft run --scale-to-zero policy=idle,cooldown-time=1000,stateful=true --metro fra -m 4G -p 443:8080/tls+http -e BOOTSTRAP_ADMIN_TOKEN="$BOOTSTRAP_ADMIN_TOKEN" --volume chromium-cdp-auth-data:/app/data --image <my-org>/chromium-cdp-auth
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud deploy --scale-to-zero idle --scale-to-zero-stateful --scale-to-zero-cooldown 1s -p 443:8080/tls+http -M 4Gi --env BOOTSTRAP_ADMIN_TOKEN="$BOOTSTRAP_ADMIN_TOKEN" --volume chromium-cdp-auth-data:/app/data .
```

The output shows the instance address and other details.

**Using the unikraft CLI (Recommended)**
```ansi title="unikraft"
metro:        fra
name:         chromium-cdp-auth-d0l6y
uuid:         debe81b0-8418-4e01-b795-b3546e0e5aac
state:        starting
image:        <my-org>/chromium-cdp-auth
resources:
  memory:     4GiB
  vcpus:      1
service:
  uuid:       516e239b-2ab1-9fb9-599d-fb891cc39edb
  name:       spring-dream-p5wxwwl0
  domains:
  - fqdn:     spring-dream-p5wxwwl0.fra.unikraft.app
networks:
- uuid:       7d3633e4-7835-942c-7b32-5d392ba538d7
  private-ip: 10.0.4.141
  mac:        12:b0:7b:d3:eb:de
timestamps:
  created:    just now
```

or

**Using the legacy kraft CLI**
```ansi title="kraft"
[●] Deployed successfully!
 │
 ├───────── name: chromium-cdp-auth-d0l6y
 ├───────── uuid: debe81b0-8418-4e01-b795-b3546e0e5aac
 ├──────── metro: https://api.fra.unikraft.cloud/v1
 ├──────── state: starting
 ├─────── domain: https://spring-dream-p5wxwwl0.fra.unikraft.app
 ├──────── image: oci://unikraft.io/<my-org>/chromium-cdp-auth@sha256:9e22546a9234efbd586b3cc3ff2ab71d64b56e87b8af431a3dfffd4aff274cc3
 ├─────── memory: 4096 MiB
 ├────── service: spring-dream-p5wxwwl0
 ├─ private fqdn: chromium-cdp-auth-d0l6y.internal
 └─── private ip: 10.0.4.141
```

In this case, the instance name is `chromium-cdp-auth-d0l6y` and the address is `https://spring-dream-p5wxwwl0.fra.unikraft.app`.
They're different for each run.

## Authentication

All CDP endpoints require a valid token, passed either as:

- **Query parameter**: `?token=<TOKEN>`
- **Authorization header**: `Authorization: Bearer <TOKEN>`

The bootstrap admin token (set via the `BOOTSTRAP_ADMIN_TOKEN` environment variable) can be used for initial setup.
Use it to create additional tokens.

### Token management API (admin only)

**Create a token:**
```bash
curl -X POST https://<instance-url>/api/tokens \
  -H "Authorization: Bearer $BOOTSTRAP_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-client", "expiresInDays": 7}'
```

**List tokens:**
```bash
curl https://<instance-url>/api/tokens \
  -H "Authorization: Bearer $BOOTSTRAP_ADMIN_TOKEN"
```

**Revoke a token:**
```bash
curl -X DELETE https://<instance-url>/api/tokens/<token> \
  -H "Authorization: Bearer $BOOTSTRAP_ADMIN_TOKEN"
```

### Public endpoints

- `GET /health` — health check (no auth required)

## Testing

To query the service you need to use a CDP client.
You can use the Python-based implementation in the `test/` directory.
See [`test/README.md`](test/README.md) for setup and a screenshot example that passes a token.

## Instance management

You can list information about the instance by running:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances list
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance list
```

When done, you can remove the instance:

**Using the unikraft CLI (Recommended)**
```bash title="unikraft"
unikraft instances delete chromium-cdp-auth-d0l6y
```

or

**Using the legacy kraft CLI**
```bash title="kraft"
kraft cloud instance remove chromium-cdp-auth-d0l6y
```

## Learn more

- [CDP Documentation](https://chromedevtools.github.io/devtools-protocol/)
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
