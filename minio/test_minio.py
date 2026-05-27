"""End-to-end test for the ``minio`` example.

Mirrors the manual steps from ``minio/README.md``:

1. ``unikraft build . --output <prefix>/minio:<tag>``
2. ``unikraft run --metro <metro> -p 443:9001/tls+http -p 9000:9000/tls -m 512M --image ...``
3. ``curl https://<instance-url>/health/live`` and assert "html".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_hugo_serves_site(build_image, run_instance, http):
    image = build_image("minio", "minio")

    instance = run_instance(
        image,
        publish=["443:9001/tls+http", "9000:9000/tls"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(f"{url}/health/live")
    assert resp.status_code == 200
    assert "html" in resp.text
