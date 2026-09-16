# CS 212 Week 5 -- reference fixtures for slot
#
# Copy what you need into your own tests/conftest.py. Nothing here is
# marked; it exists so that nobody loses an evening to the two fixtures
# every team needs and nobody has written before.
#
# Requires: pytest 8.2, psycopg 3, testcontainers[postgres] 4.x
#   (or drop the container fixture and point DATABASE_URL at a compose service)

import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


# ---------------------------------------------------------------------------
# 1. One Postgres for the whole session.  ~9 s once, not 9 s per module.
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def pg_url():
    """A real Postgres. Session-scoped: started once."""
    if url := os.environ.get("TEST_DATABASE_URL"):
        # CI supplies a service container; don't start a second one.
        yield url
        return

    from testcontainers.postgres import PostgresContainer
    with PostgresContainer("postgres:16") as pg:
        yield pg.get_connection_url()


@pytest.fixture(scope="session")
def engine(pg_url):
    eng = create_engine(pg_url, future=True)
    run_migrations(eng)          # your Alembic upgrade head
    return eng


# ---------------------------------------------------------------------------
# 2. The rollback fixture.  ~2 ms per test, perfect isolation.
#
#    LIMITATION, and it is the one that matters for A 5 Q1: this cannot be
#    used for anything that commits, which includes any test with real
#    concurrency -- two connections cannot see each other's uncommitted rows,
#    so the unique index is never exercised.  Those tests need fixture 3.
# ---------------------------------------------------------------------------

@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection, future=True)
    s = Session()
    try:
        yield s
    finally:
        s.close()
        transaction.rollback()   # everything the test did, undone
        connection.close()


# ---------------------------------------------------------------------------
# 3. For tests that must commit: truncate afterwards instead.
#    Slower (~15 ms) and used by few tests.
# ---------------------------------------------------------------------------

@pytest.fixture
def committed_db(engine):
    yield engine
    with engine.begin() as conn:
        conn.execute(text(
            "TRUNCATE bookings, resources, users RESTART IDENTITY CASCADE"))


# ---------------------------------------------------------------------------
# 4. A frozen clock.  datetime.now() inside domain code is a defect (L16 s4);
#    pass a clock in, and in tests pass this one.
# ---------------------------------------------------------------------------

from datetime import datetime, timezone

@pytest.fixture
def clock():
    class FrozenClock:
        def __init__(self, at): self.at = at
        def now(self): return self.at
        def advance(self, **kw):
            from datetime import timedelta
            self.at += timedelta(**kw)
            return self.at
    return FrozenClock(datetime(2026, 3, 4, 9, 0, tzinfo=timezone.utc))


# ---------------------------------------------------------------------------
# 5. Determinism.  If you are not running with -p randomly, you do not know
#    whether your suite is order-independent.  Put this in pyproject.toml:
#
#        [tool.pytest.ini_options]
#        addopts = "-p randomly --strict-markers"
#        markers = ["contract: hits a real external service; not in the gate"]
#
#    and expect it to fail the first time.  That failure is the point.
# ---------------------------------------------------------------------------
