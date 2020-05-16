from TFSManager import Manager as TFSManager
import SqliteManager
import datetime
import sys
from DirectoryManager import DirectoryManager

# deploy_tuple = (0,1,datetime.datetime.now())
# deploy_id = SqliteManager.insert_deploys(deploy_tuple)
# script_tuple = (deploy_id, 'benim_scriptim.sql')
# script_id = SqliteManager.insert_scripts(script_tuple)
# result_tuple = (script_id, 'No Errors')
# SqliteManager.insert_script_results(result_tuple)

def deploy():
    # tfs = TFSManager.Manager()
    # for i, arg in enumerate(sys.argv):
    #     if i == 1:
    #         project = arg
    #     elif i == 2:
    #         branch = arg
    project = 'Katilim'
    branch = 'Dev'
    manager = TFSManager(project)
    latest_id = manager.get_latest_changeset_id()
    last_changeset_from_last_deploy = SqliteManager.get_last_changeset_id()
    changeset_list = manager.get_changesets(last_changeset_from_last_deploy, latest_id)
    directory = DirectoryManager('Test')
    directory.createDirectory('./Temp')
    for changeset in changeset_list:
        changes = manager.get_changes(changeset.id)
        if manager.check_change_branch(changes, branch) == False:
            continue
        for change in changes:
            file_name = manager.get_change_file_name(change)
            file_url = manager.get_change_file_url(change)
            manager.download_file(file_url, './Temp/' + file_name)

if __name__ == '__main__':
    deploy()