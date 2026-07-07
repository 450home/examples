"""End-to-end test for the ``ruby3.2-rails`` example.

Mirrors the manual steps from ``ruby3.2-rails/README.md``:

1. ``unikraft build . --output <prefix>/ruby32-rails:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 1G -e GEM_HOME=/usr/local/bundle -e BUNDLE_APP_CONFIG=/usr/local/bundle --image ...``
3. ``curl https://<instance-url>/hello`` and assert "Hello World".
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_name, extract_instance_url


def test_ruby_rails_serves_hello(build_image, run_instance, http, wait_instance):
    image = build_image("ruby3.2-rails", "ruby3.2-rails")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="1G",
        env={"GEM_HOME": "/usr/local/bundle", "BUNDLE_APP_CONFIG": "/usr/local/bundle"},
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    wait_instance(extract_instance_name(instance), "running")

    resp = http(f"{url}/hello")
    assert resp.status_code == 200
    assert "Hello World" in resp.text
