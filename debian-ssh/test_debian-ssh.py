"""End-to-end test for the ``debian-ssh`` example.

Mirrors the manual steps from ``debian-ssh/README.md``:

1. ``unikraft build . --output <prefix>/debian-ssh:<tag>``
2. ``unikraft run --metro <metro> --scale-to-zero policy=off
   -p 2222:2222/tls -m 1G -e PUBKEY="..." --image ...``
3. Set up a socat TLS tunnel to the SSH port.
4. Connect via SSH and verify the session works.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

import pytest

from _testlib.unikraft import extract_instance_fqdn

SSH_PORT = 2222


def _generate_test_keypair(tmp_path: Path) -> tuple[Path, str]:
    """Generate a temporary Ed25519 SSH keypair for the test.

    Returns (private_key_path, public_key_string).
    """
    key_path = tmp_path / "id_ed25519"
    subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-f", str(key_path), "-N", "", "-q"],
        check=True,
    )
    pub_key = (tmp_path / "id_ed25519.pub").read_text().strip()
    return key_path, pub_key


def test_debian_ssh(build_image, run_instance, socat_tunnel, tmp_path):
    """Build, deploy, and SSH into a Debian instance."""
    private_key, public_key = _generate_test_keypair(tmp_path)

    image = build_image("debian-ssh", "debian-ssh")

    instance = run_instance(
        image,
        publish=["2222:2222/tls"],
        memory="1G",
        scale_to_zero={"policy": "off"},
        env={"PUBKEY": public_key},
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    # Set up a socat TLS tunnel to the SSH port.
    tunnel = socat_tunnel(host, SSH_PORT, SSH_PORT)

    # Retry SSH connection with back-off while the instance boots.
    last_err = None
    for _ in range(10):
        try:
            result = subprocess.run(
                [
                    "ssh",
                    "-o", "StrictHostKeyChecking=no",
                    "-o", "UserKnownHostsFile=/dev/null",
                    "-o", "ConnectTimeout=10",
                    "-i", str(private_key),
                    "-p", str(tunnel.local_port),
                    "-l", "root",
                    "127.0.0.1",
                    "echo hello-from-pytest",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                assert "hello-from-pytest" in result.stdout
                return
            last_err = RuntimeError(
                f"ssh exited {result.returncode}: {result.stderr}"
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            last_err = exc

        time.sleep(5)

    raise AssertionError(
        f"could not connect via SSH after retries: {last_err}"
    ) from last_err
