"""End-to-end test for the ``tyk`` example.

Mirrors the manual steps from ``tyk/README.md``:

1. Build and deploy the Redis instance (internal, on ``tyk-redis.internal``,
   with REDIS_PASSWORD=unikraft).
2. Build and deploy the Tyk API gateway (public, on port 443:8080/tls+http).
3. ``curl https://<instance-url>/hello`` and assert Tyk health response with
   Redis connectivity confirmed.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


REDIS_PASSWORD = "unikraft"


def test_tyk_hello(build_image, run_instance, http, wait_instance):
    # 1. Build and deploy internal Redis instance.
    # NOTE: domain must be "tyk-redis.internal" — hardcoded in tyk/rootfs/etc/tyk.conf.
    redis_image = build_image("tyk/redis", "tyk-redis")

    run_instance(
        redis_image,
        memory="256M",
        domain="tyk-redis.internal",
        scale_to_zero={"policy": "idle", "cooldown-time": "1000", "stateful": "true"},
        env={"REDIS_PASSWORD": REDIS_PASSWORD},
    )

    # 2. Build and deploy the Tyk gateway.
    tyk_image = build_image("tyk/tyk", "tyk-gw")

    tyk_instance = run_instance(
        tyk_image,
        publish=["443:8080/tls+http"],
        memory="256M",
        env={"TYK_GW_STORAGE_PASSWORD": REDIS_PASSWORD},
    )

    url = extract_instance_url(tyk_instance)
    assert url, f"could not determine instance URL from: {tyk_instance!r}"

    wait_instance(extract_instance_name(tyk_instance), "running")

    # 3. Query the /hello endpoint — Tyk returns a health-check JSON
    # with status "pass".
    resp = http(f"{url}/hello")
    assert resp.status_code == 200
    body = resp.json()
    assert body.get("status") == "pass"
    assert "Tyk" in body.get("description", "")
