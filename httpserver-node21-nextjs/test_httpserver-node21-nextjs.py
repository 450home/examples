"""End-to-end test for the ``httpserver-node21-nextjs`` example.

Mirrors the manual steps from ``httpserver-node21-nextjs/README.md``:

1. ``unikraft build . --output <prefix>/httpserver-node21-nextjs:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 768M --image ...``
3. ``curl https://<instance-url>`` and assert the Next.js app is served.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_httpserver_nextjs_serves_page(build_image, run_instance, http):
    image = build_image("httpserver-node21-nextjs", "httpserver-node21-nextjs")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="768M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(url)
    assert resp.status_code == 200
