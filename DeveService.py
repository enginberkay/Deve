import sys
from pathlib import Path
import File
import DirectoryManager
import SqlPlus
import Config
import AuthenticationManager
import Email
import ExceptionManager
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/autodeploy/<string:environment>/<string:email>/<string:changesetfiles>', methods=['GET'])
def autodeploy(environment, email, changesetfiles):
    if Config.isRequiredUserLogin() == "TRUE":
        Auth = AuthenticationManager.AccountImpersonate()
        Auth.logonUser()
    files = []
    scriptToExecute = changesetfiles.split('!')
    directory = DirectoryManager.DirectoryManager(environment)
    directory.getAllFiles(files)
    directory.prepareSpoolPath(files)
    db = SqlPlus.Oracle()
    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            files.remove(file)
    for file in files:
        for scriptName in scriptToExecute:
            if scriptName == file.name:
                db.runScriptFiles(file)

    # Preprod İşlemleri
    if environment == "PREPROD":
        for file in files:
            for scriptName in scriptToExecute:
                if scriptName == file.name:
                    directory.copyScriptToProdDbFolder(file)
        directory.copyDeployPackInfoTo09()

    db.recompileInvalidObjects()
    db.getInvalidObjects(directory.rootPath)
    invalidObjectListFile = File.File(
        "InvalidObjects.log", directory.rootPath / "InvalidObjects.log")
    invalidObjectListFile.spoolPath = invalidObjectListFile.path

    email = Email.Email(email)
    for file in files:
        for scriptName in scriptToExecute:
            if scriptName == file.name:
                email.attach(file)
    email.attach(invalidObjectListFile)
    if email.sendmail(environment):
        None
    else:
        ExceptionManager.WriteException(
            "Could not send e-mail", "Email", "DeveService.py")

    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            continue
        if file.name.upper() == directory.runLog.upper():
            continue
        for scriptName in scriptToExecute:
            if scriptName == file.name:
                directory.removeSpool(file)
    directory.removeSpool(invalidObjectListFile)
    if Config.isRequiredUserLogin() == "TRUE":
        Auth.logoffUser()
    return jsonify({'result': 'OK'})


@app.route('/print/<string:files>', methods=['GET'])
def p(files):
    fileList = files.split('!')
    for f in fileList:
        print(f)
    return jsonify({'result': 'OK'})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
