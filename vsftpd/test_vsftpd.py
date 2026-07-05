"""End-to-end test for the ``vsftpd`` example.

Mirrors the manual steps from ``vsftpd/README.md``:

1. ``unikraft build . --output <prefix>/vsftpd:<tag>``
2. ``unikraft run --metro <metro> --scale-to-zero policy=on,cooldown-time=40000,stateful=true
   -p 20:20/tls -p 21:21/tls -p 222:22/tls -p 990:990/tls -p 10100:10100/tls
   -m 1G --image ...``
3. ``lftp -u root,rootpass ftps://<host>:21`` then ``ls``
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile

import pytest

from _testlib.unikraft import extract_instance_fqdn, extract_instance_name

FTP_USER = "root"
FTP_PASSWORD = "rootpass"

# lftp is required for implicit FTPS (TLS-from-first-byte) connections.
pytestmark = pytest.mark.skipif(
    shutil.which("lftp") is None,
    reason="lftp not found on PATH (install with: apt install lftp)",
)


def _lftp(host: str, commands: str, timeout: float = 30) -> subprocess.CompletedProcess[str]:
    """Run lftp commands against the instance via implicit FTPS."""
    return subprocess.run(
        [
            "lftp",
            "-u", f"{FTP_USER},{FTP_PASSWORD}",
            f"ftps://{host}:21",
            "-e", f"{commands}; exit",
        ],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def test_vsftpd(build_image, run_instance, wait_instance):
    """Build, deploy, and exercise a vsftpd instance."""
    image = build_image("vsftpd", "vsftpd")

    instance = run_instance(
        image,
        publish=[
            "20:20/tls",
            "21:21/tls",
            "222:22/tls",
            "990:990/tls",
            "10100:10100/tls",
        ],
        memory="1G",
        extra_args=[
            "--scale-to-zero", "policy=on,cooldown-time=40000,stateful=true",
        ],
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    name = extract_instance_name(instance)
    wait_instance(name, "standby")

    result = _lftp(host, "ls")
    if result.returncode != 0:
        raise AssertionError(
            f"could not connect to vsftpd (exit={result.returncode})\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

    # ls succeeded — matches the README demonstration.
    # Additionally, verify a put/get round-trip.
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tmp:
        tmp.write("hello-from-pytest")
        tmp.flush()
        local_path = tmp.name

    result = _lftp(
        host,
        f"put {local_path} -o pytest_test.txt; "
        "cat pytest_test.txt; "
        "rm pytest_test.txt",
    )
    assert result.returncode == 0, f"lftp put/get/rm failed: {result.stderr}"
    assert "hello-from-pytest" in result.stdout
