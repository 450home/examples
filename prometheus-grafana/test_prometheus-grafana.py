"""End-to-end test for the ``prometheus-grafana`` example.

Mirrors the manual steps from ``prometheus-grafana/README.md``:

1. Create a volume for the Prometheus time-series database.
2. Fill the ``<metro>`` / ``<UKC_TOKEN>`` placeholders in the Prometheus ROM.
3. Build and deploy Prometheus (internal, no published port).
4. Build and deploy Grafana (public, on port 443:3000/tls+http) with the
   provisioning and dashboard ROMs attached.
5. Assert Grafana is healthy, the data source and dashboard were provisioned,
   and Prometheus has actually scraped instance metrics.

The final assertion is what makes this an integration test rather than two
smoke tests: querying through Grafana's data source proxy exercises
Grafana -> Prometheus over the private network, and Prometheus -> the Unikraft
Cloud metrics endpoint with a real token.
"""

from __future__ import annotations

import logging
import os
import shutil
import time

import pytest

from _testlib.unikraft import extract_instance_name, extract_instance_url

log = logging.getLogger(__name__)

EXAMPLE = "prometheus-grafana"

# The internal domain hard-coded in the checked-in datasource.yml. The test
# deploys under a run-scoped domain instead, so parallel runs don't collide.
DEFAULT_PROMETHEUS_DOMAIN = "prometheus-internal.internal"

# Prometheus scrapes every 15s; allow a generous margin for the first scrape
# plus instance boot.
SCRAPE_TIMEOUT_S = 180
SCRAPE_POLL_S = 5


def _materialise(src, dst, replacements):
    """Copy a config tree to ``dst``, substituting placeholders.

    The checked-in files carry placeholders (a real token must never be
    committed), so the ROM directories are rendered into a temporary
    directory before being uploaded.
    """
    shutil.copytree(src, dst)
    for path in sorted(p for p in dst.rglob("*") if p.is_file()):
        text = original = path.read_text()
        for old, new in replacements.items():
            text = text.replace(old, new)
        if text != original:
            path.write_text(text)
    return dst


def test_prometheus_grafana(
    build_image,
    run_instance,
    http,
    unikraft,
    request,
    test_run_id,
    wait_instance,
    repo_root,
    tmp_path,
):
    """Build, deploy, and verify the Prometheus + Grafana monitoring stack."""
    token = os.environ.get("UKC_TOKEN")
    if not token:
        pytest.skip("UKC_TOKEN is not set in the environment")

    example_dir = repo_root / EXAMPLE
    volume_name = f"prometheus-data-{test_run_id}"

    def _cleanup_volume():
        try:
            unikraft.run(["volume", "delete", volume_name], check=False)
            log.info("deleted volume %s", volume_name)
        except Exception:
            log.exception("error deleting volume %s", volume_name)

    request.addfinalizer(_cleanup_volume)

    # 1. Create the Prometheus volume.
    unikraft.run([
        "volume", "create",
        "--metro", unikraft.metro,
        f"--name={volume_name}",
        "--size=1G",
    ])

    prometheus_domain = f"{test_run_id}-prometheus.internal"

    # 2. Render the Prometheus ROM with the real metro and token.
    prometheus_rom = _materialise(
        example_dir / "prometheus" / "rom",
        tmp_path / "prometheus-rom",
        {"<metro>": unikraft.metro, "<UKC_TOKEN>": token},
    )
    rendered = (prometheus_rom / "prometheus.yml").read_text()
    assert "<UKC_TOKEN>" not in rendered, "token placeholder was not substituted"
    assert "<metro>" not in rendered, "metro placeholder was not substituted"

    # 3. Build and deploy Prometheus: internal domain, no published port.
    prometheus_image = build_image(f"{EXAMPLE}/prometheus", "pg-prometheus")

    run_instance(
        prometheus_image,
        memory="1024M",
        domain=prometheus_domain,
        volume=f"{volume_name}:/prometheus",
        rom={"dir": prometheus_rom, "at": "/etc/prometheus"},
        name=f"prometheus-{test_run_id}",
    )

    # 4. Build and deploy Grafana, pointing the provisioned data source at the
    #    run-scoped Prometheus domain.
    provisioning = _materialise(
        example_dir / "grafana" / "provisioning",
        tmp_path / "grafana-provisioning",
        {DEFAULT_PROMETHEUS_DOMAIN: prometheus_domain},
    )
    datasource = (provisioning / "datasources" / "datasource.yml").read_text()
    assert prometheus_domain in datasource, "data source URL was not rewritten"

    password = os.urandom(16).hex()
    grafana_image = build_image(f"{EXAMPLE}/grafana", "pg-grafana")

    grafana = run_instance(
        grafana_image,
        publish=["443:3000/tls+http"],
        memory="1024M",
        name=f"grafana-{test_run_id}",
        scale_to_zero={"policy": "on", "cooldown-time": "1000", "stateful": "true"},
        env={
            "GF_SECURITY_ADMIN_USER": "admin",
            "GF_SECURITY_ADMIN_PASSWORD": password,
            "GF_USERS_ALLOW_SIGN_UP": "false",
            "GF_ANALYTICS_REPORTING_ENABLED": "false",
            "GF_ANALYTICS_CHECK_FOR_UPDATES": "false",
        },
        rom=[
            {"dir": provisioning, "at": "/etc/grafana/provisioning"},
            {"dir": example_dir / "grafana" / "dashboards",
             "at": "/var/lib/grafana/dashboards"},
        ],
    )

    url = extract_instance_url(grafana)
    assert url, f"could not determine instance URL from: {grafana!r}"

    wait_instance(extract_instance_name(grafana), "standby")

    auth = ("admin", password)

    # 5a. Grafana serves its login page.
    resp = http(url)
    assert resp.status_code == 200
    assert "grafana" in resp.text.lower()

    # 5b. Grafana is healthy.
    resp = http(f"{url}/api/health")
    assert resp.status_code == 200
    assert resp.json().get("database") == "ok"

    # 5c. The data source was provisioned from datasource.yml.
    resp = http(f"{url}/api/datasources/name/Prometheus", auth=auth)
    assert resp.status_code == 200
    datasource = resp.json()
    assert datasource.get("uid") == "prometheus"
    assert datasource.get("type") == "prometheus"
    assert prometheus_domain in datasource.get("url", "")

    # 5d. The dashboard was provisioned from dashboards.yml.
    resp = http(f"{url}/api/search", params={"query": "VM Instances"}, auth=auth)
    assert resp.status_code == 200
    hits = resp.json()
    uids = {hit.get("uid") for hit in hits}
    assert "ukc-vm" in uids, f"dashboard not provisioned; search returned: {hits!r}"

    # 5e. Prometheus reached the metrics endpoint and scraped real series.
    #     Proxying through Grafana proves the private-network wiring too.
    proxy = f"{url}/api/datasources/proxy/uid/prometheus/api/v1/query"
    deadline = time.monotonic() + SCRAPE_TIMEOUT_S
    result = []
    while time.monotonic() < deadline:
        resp = http(proxy, params={"query": "instance_state"}, auth=auth)
        assert resp.status_code == 200
        payload = resp.json()
        assert payload.get("status") == "success", f"query failed: {payload!r}"
        result = payload.get("data", {}).get("result", [])
        if result:
            break
        log.info("no instance_state series yet; waiting for the next scrape")
        time.sleep(SCRAPE_POLL_S)

    # This test's own two instances are live in the account, so the endpoint
    # must report at least one series.
    assert result, (
        f"no instance_state series after {SCRAPE_TIMEOUT_S}s — "
        "Prometheus did not scrape the metrics endpoint successfully"
    )
    assert all("instance_uuid" in series.get("metric", {}) for series in result), (
        f"series missing the instance_uuid label: {result!r}"
    )
