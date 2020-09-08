from pathlib import Path
from subprocess import Popen

import pytest
from pytest_bdd import scenario, given, when, then, parsers

import DbManager
import SqliteManager
from File import File
import DeveJenkins

manager = None
project = "Katilim"
branch = 'Dev'


@scenario('../features/TfsIntegration.feature', 'son deploydan sonra ki scriplterin deployu')
def test_tfs():
    pass


@given(parsers.cfparse('tfsde "Katilim" üzerinde yetkili kullanıcı bağlantısı'))
def test_tfs_connection():
    global manager
    manager = DeveJenkins.get_tfs_manager(project)
    return manager


@given('son deployun changet idsini al')
def test_get_last_changeset_id():
    id = SqliteManager.get_last_changeset_id()
    return id


@given('tfs üzerinde ki max changeseti al')
def test_get_latest_changeset_id():
    latest_id = manager.get_latest_changeset_id()
    return latest_id


@given('başlangıç id ve bitiş id arasında ki changeset listesini doldur')
def test_fill_changeset_list(test_get_last_changeset_id, test_get_latest_changeset_id):
    start_id = test_get_last_changeset_id
    end_id = test_get_latest_changeset_id
    changeset_list = manager.get_changesets(start_id, end_id)
    return changeset_list


script_list = []


@when(parsers.parse('listede ki scriptler "Dev" ortamına ait olanlar tfs üzerinden indirilir'))
def test_download_file(test_tfs_connection, test_fill_changeset_list):
    global script_list
    DeveJenkins.extract_files_from_changes_list(branch, test_fill_changeset_list[:50], test_tfs_connection, script_list)
    DeveJenkins.download_all_files(test_tfs_connection, script_list[:2])


@then(parsers.parse('"Dev" ortamda scriptler sqlplus ile db üzerinde execute edilir'))
def test_execute_script(monkeypatch):
    def mockreturn(param):
        return "script executed", "by mocked Popen"

    monkeypatch.setattr(Popen, 'communicate', mockreturn)
    db = DbManager.Oracle('TEST')
    for file in script_list[:2]:
        file_type = File(path=Path('./Temp/' + file['file_name']), name=file['file_name'])
        file_type.spoolPath = Path('./Temp/asd.log')
    msg, error = db.runScriptFiles(file_type)
    assert msg == "script executed"


@then('sonuçlar loglanır')
def test_result_logger():
    pass
    # raise NotImplementedError
