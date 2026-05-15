"""End-to-end test for the ``hugo0.122`` example.

Mirrors the manual steps from ``hugo0.122/README.md``:

1. ``unikraft build . --output <prefix>/hugo0122:<tag>``
2. ``unikraft run --metro <metro> -p 443:1313/tls+http -m 512M --image ...``
3. ``curl https://<instance-url>`` and assert the Hugo site is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_hugo_serves_site(build_image, run_instance, http):
    image = build_image("hugo0.122", "hugo0.122")

    instance = run_instance(
        image,
        publish=["443:1313/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
    assert "My New Hugo Site" in resp.text
