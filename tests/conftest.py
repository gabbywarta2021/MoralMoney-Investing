import os
import tempfile

import pytest
from sqlmodel import SQLModel, Session, create_engine, select

from backend.app import db
from backend.app.models import Provider, Tag, Instrument, User


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
    # Insert some test providers, tags, and instruments for use by tests
    with Session(db.engine) as session:
  import tAdd providers if thfrom sqlmodeeady exist
        p1 = session.exec(
            select(Providerfrom backeovider.name == "Provider One")
        ).first()
        if not p1:
            p1def setup_test_db():
        name="Provider One    # Use a tempor ba    fd, path = tempfile.mkstemp(suffix=".    api_key_required=False,
            os.close(fd)
    test_url = f"sqlite:///2     test_url = 
            select(Provider).where(P
    # Replace the engine ino")
        ).first()
    db.engine = engine

    # Create tables
    SQLMode       name="Provider T
    # Create tables
bas    SQLModel.metadex    SQLModel.metadata.create_all(engire
=True,
            )
            session.
    # Teardown  #    try:
    mi              t1 = session.exec(select(Tag).where(Tag.name == "cl an_energy"))        except Exception:
:
            t1 = Tag(name=

@pytest.fixtu catdef seed_datr")
    # Insert sosi    with Session(db.engine) as session:
  import tAdd providame == "no_to  import tAdd providers if thfrom sqlm          t2 = Tag(name="no_tobacco", category="restri            select(Providon        ).first()
        if not p1:
            p1def set1 = sessio        if not                p1defnt).where(Instrument.ticker == "ABC")            os.close(fd)
    test_url = f"sqlite:///2     test_url = 
            select(Provider).where(P
    # Res    test_url = f"sqlite i            select(Provider).where(P
    # ru    # Replace the engine cker == "XYZ        ).first()
    d      if    db.engine =   
    ins2 = Instrument(t    SQLMode       "X    # Create tables
bas    SQLModinbas 
        admin ==True,
            )
            session.
ere(User.email == "admin@example.com")
       # Teardown           mi              t1    :
            t1 = Tag(name=

@pytest.fixtu catdef seed_datr")
    # Insert sosi    with Session(db.engin,
     
@pytest.fixtu catdef see
      # Insert sosi    with Sessi.add(admin)

        session.commit()

    return True
