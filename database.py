import os
from contextlib import contextmanager

import oracledb
from dotenv import load_dotenv

load_dotenv()

_pool: oracledb.ConnectionPool | None = None


def _dsn() -> str:
    host = os.getenv("ORACLE_HOST", "localhost")
    port = os.getenv("ORACLE_PORT", "1521")
    sid = os.getenv("ORACLE_SID", "FREE")
    return oracledb.makedsn(host, port, sid=sid)


def get_pool() -> oracledb.ConnectionPool:
    global _pool
    if _pool is None:
        _pool = oracledb.create_pool(
            user=os.getenv("ORACLE_USER"),
            password=os.getenv("ORACLE_PASSWORD"),
            dsn=_dsn(),
            min=1,
            max=5,
            increment=1,
        )
    return _pool


@contextmanager
def get_connection():
    connection = get_pool().acquire()
    try:
        yield connection
    finally:
        connection.close()


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None
