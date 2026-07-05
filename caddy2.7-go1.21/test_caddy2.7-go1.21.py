"""End-to-end test for the ``caddy2.7-go1.21`` example.

Mirrors the manual steps from ``caddy2.7-go1.21/README.md``:

1. ``unikraft build . --output <prefix>/caddy2.7-go1.21:<tag>``
2. ``unikraft run --metro <metro> -p 443:2015/http+tls -m 256M --image ...``
3. ``curl https://<instance-url>`` and assert the default Caddy welcome page.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_caddy_serves_welcome_page(build_image, run_instance, http, wait_instance):
    image = build_image("caddy2.7-go1.21", "caddy2.7-go1.21")

    instance = run_instance(
        image,
        publish=["443:2015/http+tls"],
        memory="256M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "Hello, world!" in resp.text
