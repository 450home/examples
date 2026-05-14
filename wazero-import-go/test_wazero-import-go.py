"""End-to-end test for the ``wazero-import-go`` example.

Mirrors the manual steps from ``wazero-import-go/README.md``:

1. ``unikraft build . --output <prefix>/wazero-import-go:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 512M --image ...``
3. ``curl https://<instance-url>`` and assert the WASM age calculator output.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_wazero_serves_age_output(build_image, run_instance, http):
    image = build_image("wazero-import-go", "wazero-import-go")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
    assert "log_i32 >>" in resp.text
    assert "println >>" in resp.text
