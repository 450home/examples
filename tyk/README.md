# Tyk

This example uses [`Tyk`](https://tyk.io/), an API gateway and management platform.
Tyk is used together with Redis to store API tokens and OAuth clients.

To run this example, follow these steps:

1. Install the CLI.
   Use the [unikraft CLI](https://unikraft.com/docs/cli/unikraft) or the legacy [kraft CLI](https://unikraft.org/docs/cli/install).
   You need a [BuildKit](https://github.com/moby/buildkit) builder. The easiest way to get one is via [Docker](https://docs.docker.com/engine/install/).
   Alternatively, you can also directly set up and use BuildKit, see the [quick start](https://github.com/moby/buildkit#quick-start).

2. Clone the [`examples` repository](https://github.com/unikraft-cloud/examples) and `cd` into the `examples/tyk/` directory:

```bash
git clone https://github.com/unikraft-cloud/examples
cd examples/tyk/
```

Make sure to log into Unikraft Cloud by setting your token and a [metro](https://unikraft.com/docs/platform/metros) close to you.
This guide uses `fra` (Frankfurt, 🇩🇪):

```bash
export UKC_TOKEN=token
export UKC_METRO=fra
```

When done, invoke the following command to deploy this app on Unikraft Cloud:

```bash
kraft cloud compose up
```

The Tyk and Redis instances are named `tyk-tyk` and `tyk-redis` (as defined in the `compose.yaml` file).
Only the Tyk instance is available as a public service.
Its address is `https://funky-pond-45usfkxx.fra.unikraft.app`.
It's different for each run.

Use `curl` to query the Tyk instance on Unikraft Cloud on the available address:

```bash
curl https://funky-pond-45usfkxx.fra-test.unikraft.app/hello
```

```text
{"status":"pass","version":"v5.3.0-dev","description":"Tyk GW","details":{"redis":{"status":"pass","componentType":"datastore","time":"2024-07-12T05:57:44Z"}}}
```

When done, you can bring down the instances:

```bash
kraft cloud compose down
```

## Customize your app

To customize the Tyk app, you can update:

* `Kraftfile`: the Unikraft Cloud specification
* `Dockerfile` / `rootfs/`: the Tyk filesystem (in this case the configuration file `/etc/tyk.conf`)
* `compose.yaml`: the Compose specification

It's unlikely you will have to update the `Kraftfile` specification.

Update the contents of the `rootfs/etc/tyk.conf` file for a different configuration.

You can also update the `Dockerfile` in order to extend the Tyk filesystem with extra data files or configuration files.

The `compose.yaml` file can be update to assign different names, ports, network names or other [Compose](https://unikraft.com/docs/cli/compose)-specific configurations.

## Learn more

Use the `--help` option for detailed information on using Unikraft Cloud:

```bash
kraft cloud --help
```

Or visit the [CLI Reference](https://unikraft.com/docs/cli/overview).
