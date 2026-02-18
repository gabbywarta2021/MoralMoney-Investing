import pytest

from backend.app import allocate as allocate_mod
from backend.app import auth as auth_mod


class FakeQuery:
    def __init__(self, result):
        self._result = result

    def first(self):
        return self._result

    def all(self):
        return self._result


class FakeDB:
    def __init__(self, result=None):
        self._result = result
        self.added = None

    def exec(self, _stmt):
        return FakeQuery(self._result)

    def add(self, obj):
        self.added = obj

    def commit(self):
        return None

    def refresh(self, obj):
        return None


def test_allocate_no_instruments():
    db = FakeDB(result=[])
    out = allocate_mod.allocate(db=db, suggest=True)
    assert out["items"] == []
    assert out["cash_pct"] == 20


def test_allocate_with_instruments():
    # Create simple instrument-like objects
    class Inst:
        def __init__(self, ticker):
            self.ticker = ticker

    insts = [Inst("AAA"), Inst("BBB"), Inst("CCC")]
    db = FakeDB(result=insts)
    out = allocate_mod.allocate(db=db)
    assert len(out["items"]) == 3
    # percent should be equal-weight after 20% cash buffer
    assert all(item["pct"] > 0 for item in out["items"])


def test_auth_register_and_login():
    # register should add a user to the DB
    db = FakeDB(result=None)
    payload = {"email": "x@example.com", "password": "secret"}
    ret = auth_mod.register(payload=payload, db=db)
    assert ret["email"] == "x@example.com"
    assert db.added is not None

    # login: fake db returns a user with the hashed password
    # Build a user-like object
    hashed = auth_mod.pwd_context.hash("secret")

    class U:
        def __init__(self, email, hashed_password, is_admin=False):
            self.email = email
            self.hashed_password = hashed_password
            self.is_admin = is_admin

    user = U("x@example.com", hashed)
    db2 = FakeDB(result=user)
    token = auth_mod.login(payload={"email": "x@example.com", "password": "secret"}, db=db2)
    assert token["access_token"] == "x@example.com"


def test_auth_register_missing_fields():
    db = FakeDB(result=None)
    with pytest.raises(Exception):
        auth_mod.register(payload={"email": "no-pass"}, db=db)


def test_get_current_user_and_admin_checks():
    # missing header
    db = FakeDB(result=None)
    with pytest.raises(Exception):
        auth_mod.get_current_user(db=db, authorization=None)

    # invalid token
    db2 = FakeDB(result=None)
    with pytest.raises(Exception):
        auth_mod.get_current_user(db=db2, authorization="Bearer nope")

    # admin check
    class U:
        def __init__(self, is_admin=False):
            self.is_admin = is_admin

    non_admin = U(is_admin=False)
    with pytest.raises(Exception):
        auth_mod.get_current_active_admin(current_user=non_admin)
