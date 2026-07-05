"""End-to-end test for the ``duckdb-go1.21`` example.

Mirrors the manual steps from ``duckdb-go1.21/README.md``:

1. ``unikraft build . --output <prefix>/duckdb-go121:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 256M --image ...``
3. ``curl https://<instance-url>`` and assert DuckDB query output.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_duckdb_go_serves_query_result(build_image, run_instance, http, wait_instance):
    image = build_image("duckdb-go1.21", "duckdb-go1.21")

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
    assert "42" in resp.text
    assert "John" in resp.text
