"""End-to-end test for the ``httpserver-go1.22-redis`` example.

Mirrors the manual steps from ``httpserver-go1.22-redis/README.md``:

1. Build and deploy the Redis instance (internal, on ``go122-redis-{test_run_id}.internal``,
   with REDIS_PASSWORD=unikraft).
2. Build and deploy the Go HTTP server (public, on port 443:8080/tls+http).
3. POST a key-value pair and GET it back to verify the round-trip through Redis.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


REDIS_PASSWORD = "unikraft"


def test_go_redis_set_get(build_image, run_instance, http, http_post, wait_instance, test_run_id):
    redis_domain = f"go122-redis-{test_run_id}.internal"

    # 1. Build and deploy internal Redis instance.
    redis_image = build_image("httpserver-go1.22-redis/redis", "go122-redis-db")

    redis_instance = run_instance(
        redis_image,
        memory="256M",
        extra_args=[
            "--domain", redis_domain,
            "--scale-to-zero", "policy=idle,cooldown-time=1000,stateful=true",
            "-e", f"REDIS_PASSWORD={REDIS_PASSWORD}",
        ],
    )
    wait_instance(extract_instance_name(redis_instance), "standby")

    # 2. Build and deploy the Go HTTP server.
    app_image = build_image("httpserver-go1.22-redis/httpserver-go", "go122-redis-app")

    app_instance = run_instance(
        app_image,
        publish=["443:8080/tls+http"],
        memory="256M",
        extra_args=[
            "--env", f"REDIS_ADDR={redis_domain}:6379",
            "--env", f"REDIS_PASS={REDIS_PASSWORD}",
        ],
    )

    url = extract_instance_url(app_instance)
    assert url, f"could not determine instance URL from: {app_instance!r}"

    wait_instance(extract_instance_name(app_instance), "running")

    # 3. POST a key-value pair.
    resp = http_post(url, data={"key": "pytest-key", "value": "pytest-value"})
    assert resp.status_code == 200
    assert "Success" in resp.text

    # 4. GET the value back.
    resp = http(f"{url}/?key=pytest-key")
    assert resp.status_code == 200
    assert "pytest-value" in resp.text
