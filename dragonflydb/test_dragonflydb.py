"""End-to-end test for the ``dragonflydb`` example.

Mirrors the manual steps from ``dragonflydb/README.md`` and the existing
CI workflow (example-dragonflydb-stable.yaml):

1. ``unikraft build . --output <prefix>/dragonflydb:<tag>``
2. ``unikraft run --metro <metro> -p 443:6379/http+tls -m 512M --image ...``
3. ``curl https://<instance-url>`` → HTML status page with "Status" and "OK".

DragonflyDB is deployed with ``443:6379/http+tls``, which routes all
traffic through the HTTP layer.  The Redis wire protocol cannot be used
over an HTTP port, so we only test the HTTP status page (matching the
README and CI workflow).
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_dragonflydb(build_image, run_instance, http):
    """Build, deploy, and exercise a DragonflyDB instance."""
    image = build_image("dragonflydb", "dragonflydb")

    instance = run_instance(
        image,
        publish=["443:6379/http+tls"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    # http() already retries with back-off, so no manual sleep needed.
    # ------------------------------------------------------------------
    # 1. HTTP status page — matches existing CI workflow (curl check).
    #    The README shows an HTML page containing a Dragonfly logo,
    #    "Status", "OK", engine stats, and current-time.
    # ------------------------------------------------------------------
    resp = http(url)
    assert resp.status_code == 200
    body = resp.text.lower()
    assert "dragonfly" in body and "status" in body
