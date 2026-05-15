"""End-to-end test for the ``httpserver-java17-spring-petclinic`` example.

Mirrors the manual steps from ``httpserver-java17-spring-petclinic/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-java17-spring-petclinic:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>`` and assert the PetClinic UI is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_spring_petclinic_serves_page(build_image, run_instance, http):
    image = build_image("httpserver-java17-spring-petclinic", "httpserver-java17-spring-petclinic")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
    assert "PetClinic" in resp.text
