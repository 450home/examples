"""End-to-end test for the ``github-webhook-node`` example.

Mirrors the manual steps from ``github-webhook-node/README.md``:

1. ``unikraft build . --output <prefix>/github-webhook-node:<tag>``
2. ``unikraft run --metro <metro> -p 443:3000/tls+http -m 1G --image ...``
3. ``curl https://<instance-url>/health`` and assert the health endpoint responds.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_github_webhook_health(build_image, run_instance, http):
    image = build_image("github-webhook-node", "github-webhook-node")

    instance = run_instance(
        image,
        publish=["443:3000/tls+http"],
        memory="1G",
        extra_args=[
            "-e", "GITHUB_WEBHOOK_SECRET=test_secret",
        ],
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    resp = http(f"{url}/health")
    assert resp.status_code == 200

    data = resp.json()
    assert data["status"] == "healthy"
