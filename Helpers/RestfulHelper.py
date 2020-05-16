import requests
import base64
from requests.auth import HTTPBasicAuth


class HttpClient:
    def __init__(self, userName, password, pat, authorizationRequirement = False):
        self.http_session = requests.Session()
        if authorizationRequirement == True:
            if (userName is None or password is None) and pat is None:
                    raise ValueError('User name and password or personal access token must be specified!')
            if pat is not None:
                pat = ":" + pat
                pat_base64 = b'Basic ' + base64.b64encode(pat.encode("utf8"))
                self.http_session.headers.update({'Authorization': pat_base64})
            else:
                if userName is not None and password is not None:
                    self.http_session.auth = HTTPBasicAuth(userName, password)
    def send_get(self, uri,  payload=None):
        return self.__send_request(uri, payload=payload)

    def __send_request(self, url, headers=None, payload=None):
        if payload is None:
            payload = {}
        if headers is None:
            headers = {}
        if headers.get('Content-Type') is None:
            headers['Content-Type'] = 'application/json'
        response = self.http_session.get(url, headers=headers, verify=True, params=payload)
        response.raise_for_status()
        result = response.json()
        return result


# resp = requests.get('https://azoreahai.vizyoneks.com.tr/tfs/DbCollection/_apis/tfvc/changesets/17940/changes')

# httpClient = httpClient(None,None,'jq3cp4fpbraiyd3sgkcn2ks5lgydb23hmmgkkkezkhsakuomhqka', True)
# resp = httpClient.send_get('https://azoreahai.vizyoneks.com.tr/tfs/DbCollection/_apis/tfvc/changesets/17940/changes', {'Content-Type': 'application/json'})
# print(resp)
 