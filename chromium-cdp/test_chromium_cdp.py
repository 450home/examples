"""End-to-end test for the ``chromium-cdp`` example.

Mirrors the manual steps from ``chromium-cdp/README.md``:

1. ``unikraft build . --output <prefix>/chromium-cdp:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 4G --image ...``
3. ``curl https://<instance-url>/json/version`` and assert "Browser".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_chromium_version(build_image, run_instance, http):
    image = build_image("chromium-cdp", "chromium-cdp")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="4G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(f"{url}/json/version")
    assert resp.status_code == 200
    assert "Browser" in resp.text
