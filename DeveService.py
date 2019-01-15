import sys
from pathlib import Path
import File
import DirectoryManager
import SqlPlus
import Config
import Authenticate as Auth
import Email
# import Email
from flask import Flask, jsonify, request

app = Flask(__name__)
AuthenticationManager = Auth.ImpersonateWin32Sec()

@app.route('/autodeploy/<string:environment>', methods=['GET'])
def autodeploy(environment):
    AuthenticationManager.logonUser()
    files = []
    directory = DirectoryManager.DirectoryManager(environment)
    directory.getAllFiles(files)
    directory.prepareSpoolPath(files)
    db = SqlPlus.Oracle()
    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            continue
        db.runScriptFiles(file)
    # Preprod İşlemleri
    if environment == "PREPROD":
        directory.copyScriptsToProdDbFolder(files)
        content = directory.readDeployPackInfo()
        directory.appendDeployPackInfoTo09(content)

    if Config.getMailActive() == "TRUE":
        print("Email is preparing")
        email = Email.Email(None)
        for file in files:
            if file.name.upper() == directory.deployPackInfo.upper():
                continue
            if file.name.upper() == directory.runLog.upper():
                continue
            email.attach(file)
        if email.sendmail("Test"):
            print("Email sent")
        else:
            print("Email couldn't send")

    AuthenticationManager.logoffUser()
    return jsonify({'result': 'OK'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
