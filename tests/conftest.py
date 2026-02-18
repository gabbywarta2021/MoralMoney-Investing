import os
import tempfile

import pytest
from sqlmodel import SQLModel, Session, create_engine

from backend.app import db


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Use a temporary SQLite file for tests to avoid interfering with dev.db
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    test_url = f"sqlite:///{path}"
    engine = create_engine(test_url, echo=False)

    # Replace the engine in the db module so test modules use the test engine
    db.engine = engine

    # Create tables
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    yield engine
    # Teardown
    try:
        SQLModel.metadata.drop_all(engine)
    finally:
        try:
            os.remove(path)
        except Exception:
            pass


@pytest.fixture
def seed_data():
    # Minimal seed fixture: tests can create their own users/accounts.
    # Provide an empty DB state by default.
    with Session(db.engine) as session:
        session.commit()

    return True
