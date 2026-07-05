"""End-to-end test for the ``opentelemetry-collector`` example.

Mirrors the existing CI workflow (example-opentelemetry-collector-stable.yaml):

1. ``unikraft build . --output <prefix>/opentelemetry-collector:<tag>``
2. ``unikraft run --metro <metro> -p 443:13133/tls+http -m 1536M --image ...``
3. ``curl https://<instance-url>`` → HTTP 200 from the health check extension.

Port 13133 is the OpenTelemetry Collector's health_check extension endpoint.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_opentelemetry_collector(build_image, run_instance, http, wait_instance):
    """Build, deploy, and verify the OTel Collector health check responds."""
    image = build_image("opentelemetry-collector", "opentelemetry-collector")

    instance = run_instance(
        image,
        publish=["443:13133/tls+http"],
        memory="1536M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
