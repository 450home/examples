"""End-to-end test for the ``traefik`` example.

Mirrors the manual steps from ``traefik/README.md`` and the existing
CI workflow (example-traefik-stable.yaml):

1. ``unikraft build . --output <prefix>/traefik:<tag>``
2. ``unikraft run --metro <metro> -p 443:80/tls+http -p 8080:8080/tls
   -m 1G --image ...``
3. ``curl https://<instance-url>:8080/dashboard/`` → Traefik dashboard HTML.
"""

from __future__ import annotations

from urllib.parse import urlparse

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_traefik_dashboard(build_image, run_instance, http, wait_instance):
    """Build, deploy, and verify the Traefik dashboard is accessible."""
    image = build_image("traefik", "traefik")

    instance = run_instance(
        image,
        publish=["443:80/tls+http", "8080:8080/tls"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    # The old workflow and README test the dashboard on port 8080.
    parsed = urlparse(url)
    dashboard_url = f"https://{parsed.hostname}:8080/dashboard/"

    resp = http(dashboard_url)
    assert resp.status_code == 200
    body = resp.text.lower()
    assert "traefik" in body
