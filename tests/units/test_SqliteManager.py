from datetime import datetime
import pytest
import SqliteManager
from Models.ScriptResultsTableModel import ScriptResultsTableModel
from Models.ScriptsTableModel import ScriptsTableModel
from Models.DeploysTableModel import DeploysTableModel


def test_get_last_changeset_id():
    id = SqliteManager.get_last_changeset_id()
    assert id == 1


def test_insert_deploy():
    deploy = DeploysTableModel(0, 1, datetime.now())
    SqliteManager.insert_deploy(tuple(deploy))


def test_insert_scripts():
    script = ScriptsTableModel(1, "any.sql")
    SqliteManager.insert_scripts(tuple(script))


def test_insert_script_results():
    script_result = ScriptResultsTableModel(1, "No Errors!")
    SqliteManager.insert_script_results(tuple(script_result))
