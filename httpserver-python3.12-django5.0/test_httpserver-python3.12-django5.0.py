"""End-to-end test for the ``httpserver-python3.12-django5.0`` example.

Mirrors the manual steps from ``httpserver-python3.12-django5.0/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-python312-django50:<tag>``
2. ``unikraft run --metro <metro> -p 443:80/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>/admin/`` and assert the Django admin is served.

The default Django project only defines the ``/admin/`` URL pattern, so we
test that endpoint rather than the root.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_django_serves_admin(build_image, run_instance, http):
    image = build_image("httpserver-python3.12-django5.0", "httpserver-python3.12-django5.0")

    instance = run_instance(
        image,
        publish=["443:80/tls+http"],
        memory="1G",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(f"{url}/admin/", expected_status=200)
    assert resp.status_code == 200
    assert "Django" in resp.text
