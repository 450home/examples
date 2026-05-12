"""End-to-end test for the ``httpserver-rust-trunkrs-leptos`` example.

Mirrors the manual steps from ``httpserver-rust-trunkrs-leptos/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-rust-trunkrs-leptos:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 256M --image ...``
3. ``curl https://<instance-url>`` and assert the Leptos app is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_httpserver_rust_leptos_serves_page(build_image, run_instance, http):
    image = build_image("httpserver-rust-trunkrs-leptos", "httpserver-rust-trunkrs-leptos")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="256M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
