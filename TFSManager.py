from Helpers.RestfulHelper import HttpClient
from tfs import TFSAPI
import Config
import DirectoryManager


class Manager:
    def __init__(self, project):
        self.project = project
        pat = Config.getTfsPat()
        tfs_url = Config.getTfsUrl()
        self.restClient = HttpClient(None, None, pat, True)
        self.tfsClient = TFSAPI(tfs_url, pat=pat, project=project, verify=True)

    def get_latest_changeset_id(self):
        changeset = self.tfsClient.get_changesets(top=1)
        return changeset[0].changesetId

    def get_changesets(self, from_, to_):
        return self.tfsClient.get_changesets(from_=from_, to_=to_)

    def get_changeset(self, id):
        return self.tfsClient.get_changeset(id)

    def __get_changeset_changes_links(self, id):
        var = self.tfsClient.get_changeset(id)
        return var['_links']['changes']['href']

    def get_changes(self, id):
        changes_link = self.__get_changeset_changes_links(id)
        resp = self.restClient.send_get(changes_link)
        return resp['value']
    
    def check_change_branch(self, changes, branch):
        branch_path = '$/' + self.project + '/' + branch
        index = changes[0]['item']['path'].find(branch_path)
        return index > -1

    def get_change_file_url(self, change):
        return change['item']['url']
    
    def get_change_file_name(self, change):
        return DirectoryManager.get_filename(change['item']['path'])

    def download_file(self, url, filePath):
        self.tfsClient.download_file(url, filePath)