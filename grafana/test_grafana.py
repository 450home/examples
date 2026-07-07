"""End-to-end test for the ``grafana`` example.

Mirrors the manual steps from ``grafana/README.md`` and the existing
CI workflow (example-grafana-stable.yaml):

1. ``unikraft build . --output <prefix>/grafana:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 2G --image ...``
3. ``curl https://<instance-url>`` → Grafana login page (HTTP 200).
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_grafana(build_image, run_instance, http, wait_instance):
    """Build, deploy, and verify Grafana serves its login page."""
    image = build_image("grafana", "grafana")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="2G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200
    body = resp.text.lower()
    assert "grafana" in body

    # Grafana exposes a JSON health endpoint.
    resp_health = http(f"{url}/api/health")
    assert resp_health.status_code == 200
    body = resp_health.json()
    assert body.get("database") == "ok"
