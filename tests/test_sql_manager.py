import pytest
import SqliteManager

def test_get_last_changeset_id():
    id = SqliteManager.get_last_changeset_id()
    assert id == 1