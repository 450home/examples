"""End-to-end test for the ``imaginary`` example.

Mirrors the manual steps from ``imaginary/README.md`` and the existing
CI workflow (example-imaginary-stable.yaml):

1. ``unikraft build . --output <prefix>/imaginary:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 512M --image ...``
3. ``curl https://<instance-url>/health`` → JSON health status.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_imaginary(build_image, run_instance, http):
    """Build, deploy, and verify Imaginary's health endpoint."""
    image = build_image("imaginary", "imaginary")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    # The old workflow checks /health; the README shows it returns JSON
    # with fields like "uptime", "allocatedMemory", "goroutines", etc.
    resp = http(f"{url}/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "uptime" in data
    assert "goroutines" in data

    # The /form endpoint serves an HTML UI for testing image operations.
    resp_form = http(f"{url}/form")
    assert resp_form.status_code == 200
    assert "<html" in resp_form.text.lower()
