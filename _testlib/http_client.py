"""HTTP helpers shared by tests."""

from __future__ import annotations

import logging
import os
import time

import requests
import urllib3

log = logging.getLogger(__name__)


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def allow_insecure() -> bool:
    """Return ``True`` if ``UKC_ALLOW_INSECURE`` is set to a truthy value.

    When enabled, HTTP helpers disable TLS certificate verification and
    suppress the associated urllib3 warnings. Useful for local or staging
    deployments that use self-signed certificates.
    """
    return _truthy(os.environ.get("UKC_ALLOW_INSECURE"))


if allow_insecure():
    # Silence the flood of warnings that would otherwise appear for every
    # request against a self-signed endpoint.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    log.warning(
        "UKC_ALLOW_INSECURE is set; TLS certificate verification is DISABLED"
    )


def http_get(
    url: str,
    *,
    timeout: float = 10.0,
    retries: int = 10,
    backoff: float = 2.0,
    expected_status: int | None = 200,
    verify: bool | str | None = None,
    **kwargs,
) -> requests.Response:
    """GET ``url`` with retries while the instance warms up.

    Retries on connection errors and on non-matching status codes (when
    ``expected_status`` is provided). Raises the last exception if all
    attempts fail.

    If ``verify`` is not explicitly provided and ``UKC_ALLOW_INSECURE`` is
    set, TLS verification is disabled.
    """
    if verify is None:
        verify = not allow_insecure()

    last_exc: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            log.info("GET %s (attempt %d/%d)", url, attempt, retries)
            resp = requests.get(
                url, timeout=timeout, verify=verify, **kwargs
            )

            if expected_status is None or resp.status_code == expected_status:
                return resp
            
            log.warning(
                "unexpected status %d from %s, retrying", resp.status_code, url
            )

            last_exc = AssertionError(
                f"GET {url} returned {resp.status_code}, expected {expected_status}"
            )
        except requests.RequestException as exc:
            log.warning("GET %s failed: %s", url, exc)
            last_exc = exc
            
        if attempt < retries:
            time.sleep(backoff)

    assert last_exc is not None
    raise last_exc
