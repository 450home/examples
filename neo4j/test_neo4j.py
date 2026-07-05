"""End-to-end test for the ``neo4j test`` example.

Mirrors the manual steps from ``neo4j/README.md``:

1. ``unikraft build . --output <prefix>/neo4j:<tag>``
2. ``unikraft run --metro <metro> --scale-to-zero policy=idle,cooldown-time=4000,stateful=true -m 2G -p 443:7474/tls+http -p 7687:7687/tls ---image ...``
3. ``curl https://<instance-url>`` and assert "neo4j_edition".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_httpserver_flask_serves_hello(build_image, run_instance, http, wait_instance):
    image = build_image("neo4j", "neo4j")

    instance = run_instance(
        image,
        publish=["443:7474/tls+http", "7687:7687/tls"],
        memory="2G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(url)
    assert resp.status_code == 200

    assert '"neo4j_edition":"community"' in resp.text
