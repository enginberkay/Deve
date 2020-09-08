import pytest
import TFSManager
import os

manager = TFSManager.Manager("Katilim")

_latest_changeset_id = 0

def get_latest_changeset_id():
    global _latest_changeset_id
    if _latest_changeset_id == 0:
        _latest_changeset_id = manager.get_latest_changeset_id()
    return _latest_changeset_id

_changes = None
def get_changes_for_test():
    global _changes
    if _changes == None:
        # get_latest_changeset_id()
        # _changes = manager.get_changes(get_latest_changeset_id())
        _changes = manager.get_changes(21820)
    return _changes

def test_download_file_with_tfsapi():
    url = 'https://azoreahai.vizyoneks.com.tr/tfs/DbCollection/_apis/tfvc/items/$/Ziraat/Test/Scripts/257811_nesneleri_olustur.sql?versionType=Changeset&version=19302'
    filePath = './script'
    manager.download_file(url, filePath)
    assert os.path.exists(filePath) == True
    os.remove(filePath)


def test_get_latest_changeset_id():
    id = manager.get_latest_changeset_id()
    assert id != None


def test_get_changesets():
    id = get_latest_changeset_id()
    changeset_list = manager.get_changesets(id, id)
    assert changeset_list.__len__() == 1


def test_get_changes():
    id = get_latest_changeset_id()
    changes = manager.get_changes(id)
    assert changes != None


def test_get_change_url():
    changes = get_changes_for_test()
    for change in changes:
        url = manager.get_change_file_url(change)
    assert url != None


def test_get_change_file_name():
    changes = get_changes_for_test()
    for change in changes:
        url = manager.get_change_file_name(change)
    assert url != None

def test_check_change_branch():
    changes = get_changes_for_test()
    result = manager.check_change_branch(changes, 'Test')
    assert result == True