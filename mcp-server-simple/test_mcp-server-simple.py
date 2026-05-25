"""End-to-end test for the ``mcp-server-simple`` example.

Mirrors the manual steps from ``mcp-server-simple/README.md``:

1. ``unikraft build . --output <prefix>/mcp-server-simple:<tag>``
2. ``unikraft run --metro <metro> -p 443:8080/tls+http -m 512M --image ...``
3. Connect to the MCP server endpoint and verify it responds.

The MCP server exposes its HTTP transport at ``/mcp``.  We verify the
server is reachable by issuing an MCP ``initialize`` request.
"""

from __future__ import annotations

from _testlib.unikraft import extract_instance_url


def test_mcp_server_simple_responds(build_image, run_instance, http_post):
    image = build_image("mcp-server-simple", "mcp-server-simple")

    instance = run_instance(
        image,
        publish=["443:8080/tls+http"],
        memory="512M",
    )

    url = extract_instance_url(instance)
    assert url, f"could not determine instance URL from: {instance!r}"

    # Send an MCP initialize request to the server's HTTP transport endpoint.
    resp = http_post(
        f"{url}/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "pytest", "version": "1.0.0"},
            },
        },
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        timeout=30,
    )
    assert resp.status_code == 200
