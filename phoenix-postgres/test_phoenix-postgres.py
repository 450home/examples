"""End-to-end test for the ``phoenix-postgres`` example.

Mirrors the manual steps from ``phoenix-postgres/README.md``:

1. Create a volume for PostgreSQL data persistence.
2. Build and deploy the PostgreSQL instance (internal, on ``postgres-{test_run_id}.internal``).
3. Build and deploy the Phoenix instance (public, on port 443:4000/tls+http).
4. ``curl https://<instance-url>`` and assert Phoenix is serving pages.
"""

from __future__ import annotations

import logging
import uuid

from _testlib.unikraft import extract_instance_url

log = logging.getLogger(__name__)

PG_PASSWORD = "unikraft"
PG_USER = "postgres"
PG_DB = "myapp_prod"


def test_phoenix_postgres(build_image, run_instance, http, unikraft, request, test_run_id):
    volume_name = f"phoenix-pytest-db-data-{test_run_id}"

    def _cleanup_volume():
        try:
            unikraft.run(["volume", "delete", volume_name], check=False)
            log.info("deleted volume %s", volume_name)
        except Exception:
            log.exception("error deleting volume %s", volume_name)

    request.addfinalizer(_cleanup_volume)

    # 1. Create the PostgreSQL volume.
    unikraft.run([
        "volume", "create",
        "--metro", unikraft.metro,
        f"--name={volume_name}",
        "--size=512M",
    ])

    pg_domain = f"postgres-{test_run_id}.internal"

    # 2. Build and deploy the PostgreSQL instance.
    pg_image = build_image("phoenix-postgres/postgres", "phoenix-pg-db")

    run_instance(
        pg_image,
        memory="2G",
        extra_args=[
            "--domain", pg_domain,
            "--scale-to-zero", "policy=idle,cooldown-time=1000,stateful=true",
            "--volume", f"{volume_name}:/var/lib/postgresql/data",
            "--env", f"POSTGRES_USER={PG_USER}",
            "--env", f"POSTGRES_PASSWORD={PG_PASSWORD}",
            "--env", f"POSTGRES_DB={PG_DB}",
            "--env", "PGDATA=/var/lib/postgresql/data/pgdata",
        ],
    )

    # 3. Build and deploy the Phoenix app.
    # Generate a secret key for Phoenix.
    secret_key = uuid.uuid4().hex + uuid.uuid4().hex + uuid.uuid4().hex
    database_url = f"ecto://{PG_USER}:{PG_PASSWORD}@{pg_domain}:5432/{PG_DB}"

    phoenix_image = build_image("phoenix-postgres/phoenix", "phoenix-pg-app")

    phoenix_instance = run_instance(
        phoenix_image,
        publish=["443:4000/tls+http"],
        memory="2G",
        extra_args=[
            "--env", f"SECRET_KEY_BASE={secret_key}",
            "--env", f"DATABASE_URL={database_url}",
        ],
    )

    url = extract_instance_url(phoenix_instance)
    assert url, f"could not determine instance URL from: {phoenix_instance!r}"

    # 4. Verify Phoenix is serving.
    resp = http(url)
    assert resp.status_code == 200
    body = resp.text.lower()
    assert "phoenix" in body or "<!doctype html>" in body
