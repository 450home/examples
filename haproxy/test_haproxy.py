"""End-to-end test for the ``haproxy`` example.

Mirrors the manual steps from ``haproxy/README.md``:

1. ``unikraft build . --output <prefix>/haproxy:<tag>``
2. ``unikraft run --metro <metro> -p 443:8404/tls+http -m 256M --image ...``
3. Point browser at the ``/stats`` endpoint and verify the HAProxy stats page.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_haproxy_stats_page(build_image, run_instance, http):
    image = build_image("haproxy", "haproxy")

    instance = run_instance(
        image,
        publish=["443:8404/tls+http"],
        memory="256M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(f"{url}/stats")
    assert resp.status_code == 200
    assert "HAProxy" in resp.text
