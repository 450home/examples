"""End-to-end test for the ``MySQL`` example.

Mirrors the manual steps from ``mysql/README.md``:

1. ``unikraft build . --output <prefix>/mysql:<tag>``
2. ``unikraft run --metro <metro> -p 3306:3306/tls -m 1G
   -e MYSQL_ROOT_PASSWORD=unikraft --image ...``
3. Connect with a MySQL client (here via ``pymysql``) and run queries.

The README demonstrates:
  ``mysql -h 127.0.0.1 --ssl-mode=DISABLED -u root -punikraft mysql
    <<< "select count(*) from user"``
We replicate that query and add a round-trip table test.
"""

from __future__ import annotations

import time

import pymysql

from _testlib.unikraft import extract_instance_fqdn

MYSQL_USER = "root"
MYSQL_PASSWORD = "unikraft"
MYSQL_DATABASE = "mysql"
MYSQL_PORT = 3306


def _connect(port: int):
    """Open a plaintext PyMySQL connection through the socat TLS tunnel."""
    return pymysql.connect(
        host="127.0.0.1",
        port=port,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        connect_timeout=30,
    )


def test_mysql(build_image, run_instance, socat_tunnel):
    """Build, deploy, and exercise a MySQL instance."""
    image = build_image("mysql", "mysql")

    instance = run_instance(
        image,
        publish=["3306:3306/tls"],
        memory="1G",
        env={"MYSQL_ROOT_PASSWORD": MYSQL_PASSWORD},
    )

    host = extract_instance_fqdn(instance)
    assert host, f"could not determine instance FQDN from: {instance!r}"

    # Use a socat TLS tunnel, mirroring the README approach.
    # The platform's /tls port mapping wraps the entire TCP stream in TLS,
    # while MySQL inside speaks plain MySQL protocol.
    tunnel = socat_tunnel(host, MYSQL_PORT, MYSQL_PORT)

    # Retry the connection with back-off while MySQL finishes
    # first-boot initialisation (system tables, timezone import, etc.).
    # pymysql has no built-in retry; connect() is eager and cleans up
    # its socket on failure, so no leak on the except path.
    conn = None
    last_err = None
    for _ in range(6):
        try:
            conn = _connect(tunnel.local_port)
            break
        except pymysql.err.OperationalError as exc:
            last_err = exc
            time.sleep(10)
    if conn is None:
        raise AssertionError(
            f"could not connect to MySQL after retries: {last_err}"
        ) from last_err
    try:
        cur = conn.cursor()

        # ------------------------------------------------------------------
        # 1. SELECT count(*) FROM user — matches the README demo.
        # ------------------------------------------------------------------
        cur.execute("SELECT count(*) FROM user;")
        row = cur.fetchone()
        assert row is not None
        count = row[0]
        assert isinstance(count, int) and count > 0, (
            f"expected at least one user row, got {count}"
        )

        # ------------------------------------------------------------------
        # 2. Round-trip: CREATE → INSERT → SELECT → DROP.
        # ------------------------------------------------------------------
        cur.execute("CREATE DATABASE IF NOT EXISTS pytest_test;")
        cur.execute("USE pytest_test;")

        cur.execute(
            "CREATE TABLE t ("
            "  id INT AUTO_INCREMENT PRIMARY KEY,"
            "  name VARCHAR(64) NOT NULL"
            ");"
        )
        cur.execute("INSERT INTO t (name) VALUES ('alice'), ('bob');")
        conn.commit()

        cur.execute("SELECT name FROM t ORDER BY id;")
        rows = cur.fetchall()
        assert [r[0] for r in rows] == ["alice", "bob"]

        cur.execute("DROP DATABASE pytest_test;")
        conn.commit()

        cur.close()
    finally:
        conn.close()
