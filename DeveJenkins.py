from pathlib import Path

from File import File
from TFSManager import Manager as TFSManager
import SqliteManager
from DirectoryManager import DirectoryManager
from DbManager import Oracle

# deploy_tuple = (0,1,datetime.datetime.now())
# deploy_id = SqliteManager.insert_deploys(deploy_tuple)
# script_tuple = (deploy_id, 'benim_scriptim.sql')
# script_id = SqliteManager.insert_scripts(script_tuple)
# result_tuple = (script_id, 'No Errors')
# SqliteManager.insert_script_results(result_tuple)

manager = None


def write_spools_to_db(script_list):
    pass


def deploy():
    # tfs = TFSManager.Manager()
    # for i, arg in enumerate(sys.argv):
    #     if i == 1:
    #         project = arg
    #     elif i == 2:
    #         branch = arg
    project = 'Katilim'
    branch = 'Dev'
    tfs_manager = get_tfs_manager(project)
    latest_id = tfs_manager.get_latest_changeset_id()
    last_changeset_id_from_db = SqliteManager.get_last_changeset_id()
    changeset_list = tfs_manager.get_changesets(last_changeset_id_from_db, latest_id)
    # directory = DirectoryManager('Test')

    script_list = []
    extract_files_from_changes_list(branch, changeset_list, tfs_manager, script_list)
    download_all_files(tfs_manager, script_list)
    execute_scripts(branch, script_list)
    write_spools_to_db(script_list)


def get_tfs_manager(project):
    global manager
    manager = TFSManager(project)
    return manager


def download_all_files(tfs_manager, script_list):
    DirectoryManager.createDirectory('./Temp')
    for file in script_list:
        tfs_manager.download_file(file.file_url, file.path)


def extract_files_from_changes_list(branch, changeset_list, manager, script_list):
    for changeset in changeset_list:
        changes = manager.get_changes(changeset.id)
        if manager.check_change_branch(changes, branch) == False:
            continue
        for change in changes:
            file_name = manager.get_change_file_name(change)
            file_url = manager.get_change_file_url(change)
            script_list.append(File(name=file_name, file_url=file_url, path=Path("./Temp/" + file_name)))


def execute_scripts(branch, script_list):
    db = Oracle(branch)
    for script in script_list:
        execution_result, errorMessage = db.runScriptFiles(script)
        #Todo: jenkins için spool file bilgilendirmesi yapılacak

if __name__ == '__main__':
    deploy()
