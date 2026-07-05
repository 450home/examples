"""End-to-end test for the ``httpserver-c-debug`` example.

Mirrors the manual steps from ``httpserver-c-debug/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-c-debug:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 256M --image ...``
3. ``curl https://<instance-url>`` and assert "Hello, World!".

Note: The README also demonstrates debug ports and env vars (PUBKEY,
USE_STRACE). This test only validates the basic HTTP endpoint.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_c_debug_serves_hello(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-c-debug", "httpserver-c-debug")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="256M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    assert "Hello, World!" in resp.text
