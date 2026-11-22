
import pytest
from peewee import SqliteDatabase

from database.members.members_model import Members


@pytest.fixture
def test_db():
    db = SqliteDatabase(
        ":memory:",
        pragmas={"foreign_keys": 1},
    )

    with db.bind_ctx([Members]):
        db.connect()
        
        db.create_tables([Members])

        yield db

        db.drop_tables([Members])
        db.close()
