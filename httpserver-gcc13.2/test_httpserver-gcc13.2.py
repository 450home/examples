"""End-to-end test for the ``httpserver-gcc13.2`` example.

Mirrors the manual steps from ``httpserver-gcc13.2/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-gcc132:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 256M --image ...``
3. ``curl https://<instance-url>`` and assert "Hello, World!".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_gcc_serves_hello(build_image, run_instance, http, wait_instance):
    image = build_image("httpserver-gcc13.2", "httpserver-gcc13.2")

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
