"""End-to-end test for the ``skipper0.18`` example.

Mirrors the manual steps from ``skipper0.18/README.md`` and the existing
CI workflow (example-skipper0.18-stable.yaml):

1. ``unikraft build . --output <prefix>/skipper018:<tag>``
2. ``unikraft run --metro <metro> -p 443:9090/tls+http -m 256M --image ...``
3. ``curl https://<instance-url>`` → "Hello, world from Skipper on Unikraft!"
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_skipper(build_image, run_instance, http):
    """Build, deploy, and verify Skipper serves its configured response."""
    image = build_image("skipper0.18", "skipper018")

    instance = run_instance(
        image,
        publish=["443:9090/tls+http"],
        memory="256M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
    assert "Hello, world from Skipper on Unikraft!" in resp.text

    # The eskip routes also define a catch-all 404.
    resp_notfound = http(
        f"{url}/nonexistent",
        expected_status=None,  # disable retry on non-200
    )
    assert resp_notfound.status_code == 404
    assert "No route entry" in resp_notfound.text
