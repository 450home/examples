"""Helpers for creating TLS tunnels via ``socat``.

Some Unikraft Cloud examples expose non-HTTP services behind ``/tls`` port
mappings.  The platform wraps the entire TCP stream in TLS from the first
byte, but many client libraries (e.g. pymysql) expect to negotiate TLS at
the application protocol level (STARTTLS).  ``socat`` bridges the gap by
terminating TLS locally and exposing a plaintext TCP port.

This mirrors the ``socat`` command shown in the example READMEs::

    socat TCP-LISTEN:<local>,reuseaddr,fork OPENSSL:<host>:<port>,verify=0
"""

from __future__ import annotations

import logging
import os
import signal
import subprocess

log = logging.getLogger(__name__)


class SocatTunnel:
    """Manages a ``socat`` TLS tunnel running in the background.

    ``local_port`` is the TCP port socat will listen on locally.  The caller
    chooses a fixed port so there is no TOCTOU race from ephemeral-port
    discovery.

    Can be used as a context manager::

        with SocatTunnel(remote_host, remote_port, 17550) as tunnel:
            conn = my_connect("127.0.0.1", tunnel.local_port)
            ...

    Or via explicit ``open()`` / ``close()`` (used by the pytest fixture)::

        tunnel = SocatTunnel(host, port, 17550)
        tunnel.open()
        try:
            ...
        finally:
            tunnel.close()

    On close the ``socat`` process is terminated (with a bounded wait and
    a ``SIGKILL`` fallback so the test suite never hangs).
    """

    def __init__(self, host: str, port: int, local_port: int) -> None:
        self.host = host
        self.port = port
        self.local_port = local_port
        self._proc: subprocess.Popen | None = None

    # -- explicit lifecycle -------------------------------------------------

    def open(self) -> int:
        """Start the socat process and return the local port."""

        # start_new_session=True puts socat in its own process group so
        # close() can kill the parent *and* any forked children.
        self._proc = subprocess.Popen(
            [
                "socat",
                f"TCP-LISTEN:{self.local_port},reuseaddr,fork",
                f"OPENSSL:{self.host}:{self.port},verify=0",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        return self.local_port

    def close(self) -> None:
        """Terminate the socat process group (with SIGKILL fallback)."""
        if self._proc is None:
            return

        # Kill the entire process group (parent + forked children).
        try:
            pgid = os.getpgid(self._proc.pid)
        except ProcessLookupError:
            log.debug("socat process (pid %d) already exited", self._proc.pid)
            self._proc = None
            return

        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            log.debug("socat process group %d already exited before SIGTERM", pgid)

        try:
            _, stderr = self._proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(pgid, signal.SIGKILL)
            except ProcessLookupError:
                log.debug("socat process group %d already exited before SIGKILL", pgid)
            try:
                _, stderr = self._proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                log.warning(
                    "socat process %d still alive after SIGKILL; giving up",
                    self._proc.pid,
                )
                self._proc = None
                return

        if stderr:
            log.debug("socat stderr: %s", stderr.decode(errors="replace"))

        self._proc = None

    # -- context manager ----------------------------------------------------

    def __enter__(self) -> "SocatTunnel":
        self.open()
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()
