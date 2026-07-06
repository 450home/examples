"""End-to-end test for the ``postgres`` example.

Mirrors the manual steps from ``postgres/README.md`` and the existing
CI workflow (example-postgres-stable.yaml):

1. ``unikraft build . --output <prefix>/postgres:<tag>``
2. ``unikraft run --metro <metro> -p 5432:5432/tls -m 1G
   -e POSTGRES_PASSWORD=unikraft --image ...``
3. Connect with ``psql`` (here via ``psycopg2``) and run ``SELECT 1;``.
4. Exercise basic SQL: CREATE TABLE, INSERT, SELECT, DROP TABLE.
"""

from __future__ import annotations

import time

import psycopg2

from _testlib.unikraft import extract_instance_fqdn

# The README deploys with POSTGRES_PASSWORD=unikraft.
PG_USER = "postgres"
PG_PASSWORD = "unikraft"
PG_DATABASE = "postgres"
PG_PORT = 5432


def _connect(host: str):
    """Open a psycopg2 connection to the instance over TLS."""
    return psycopg2.connect(
        host=host,
        port=PG_PORT,
        user=PG_USER,
        password=PG_PASSWORD,
        dbname=PG_DATABASE,
        sslmode="require",
        connect_timeout=30,
    )


def test_postgres(build_image, run_instance):
    """Build, deploy, and exercise a PostgreSQL instance."""
    image = build_image("postgres", "postgres")

    instance = run_instance(
        image,
        publish=["5432:5432/tls"],
        memory="1G",
        env={"POSTGRES_PASSWORD": PG_PASSWORD},
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    # Retry the connection with back-off while PostgreSQL finishes
    # first-boot initialisation.
    # psycopg2 has no built-in retry; connect() is eager and the C
    # extension cleans up the libpq connection on failure, so no leak.
    conn = None
    last_err = None
    for _ in range(10):
        try:
            conn = _connect(host)
            break
        except psycopg2.OperationalError as exc:
            last_err = exc
            time.sleep(5)
    if conn is None:
        raise AssertionError(
            f"could not connect to PostgreSQL after retries: {last_err}"
        ) from last_err
    try:
        conn.autocommit = True
        cur = conn.cursor()

        # ------------------------------------------------------------------
        # 1. SELECT 1 — matches the existing CI workflow assertion.
        # ------------------------------------------------------------------
        cur.execute("SELECT 1;")
        row = cur.fetchone()
        assert row is not None and row[0] == 1

        # ------------------------------------------------------------------
        # 2. Server version — verify we're talking to PostgreSQL.
        # ------------------------------------------------------------------
        cur.execute("SELECT version();")
        version_str = cur.fetchone()[0]
        assert "PostgreSQL" in version_str

        # ------------------------------------------------------------------
        # 3. Round-trip: CREATE TABLE → INSERT → SELECT → DROP TABLE.
        # ------------------------------------------------------------------
        cur.execute("""
            CREATE TABLE pytest_test (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """)
        cur.execute(
            "INSERT INTO pytest_test (name) VALUES (%s), (%s);",
            ("alice", "bob"),
        )
        cur.execute("SELECT name FROM pytest_test ORDER BY id;")
        rows = cur.fetchall()
        assert [r[0] for r in rows] == ["alice", "bob"]

        cur.execute("DROP TABLE pytest_test;")

        cur.close()
    finally:
        conn.close()
