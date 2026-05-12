"""End-to-end test for the ``spin-wagi-http`` example.

Mirrors the manual steps from ``spin-wagi-http/README.md``:

1. ``unikraft build . --output <prefix>/spin-wagi-http:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 4G --image ...``
3. ``curl https://<instance-url>/hello`` and assert "Hello, Fermyon!".
4. ``curl https://<instance-url>/goodbye`` and assert "Goodbye, Fermyon!".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_spin_wagi_serves_hello_and_goodbye(build_image, run_instance, http):
    image = build_image("spin-wagi-http", "spin-wagi-http")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="4G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp_hello = http(f"{url}/hello")
    assert resp_hello.status_code == 200
    assert "Hello, Fermyon!" in resp_hello.text

    resp_goodbye = http(f"{url}/goodbye")
    assert resp_goodbye.status_code == 200
    assert "Goodbye, Fermyon!" in resp_goodbye.text
