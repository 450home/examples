"""End-to-end test for the ``wordpress-all-in-one`` example.

Mirrors the manual steps from ``wordpress-all-in-one/README.md``:

1. ``unikraft build . --output <prefix>/wordpress-all-in-one:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 4G --image ...``
3. ``curl https://<instance-url>`` and assert WordPress is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_wordpress_serves_page(build_image, run_instance, http, wait_instance):
    image = build_image("wordpress-all-in-one", "wordpress-all-in-one")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="4G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "WordPress" in resp.text
