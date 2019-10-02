import sys
from pathlib import Path
import File
import DirectoryManager
import DbManager
import Config
import AuthenticationManager
import Email
import ExceptionManager
from flask import Flask, jsonify, request

app = Flask(__name__)


def getPathModifiedDate(el):
    return Path(el.path).stat().st_mtime


@app.route('/autodeploy/<string:environment>/<string:email>/<string:changesetfiles>', methods=['GET'])
def autodeploy(environment, email, changesetfiles):
    environment = environment.upper()
    if Config.isRequiredUserLogin() == "TRUE":
        Auth = AuthenticationManager.AccountImpersonate()
        Auth.logonUser()
    files = []
    spoolsFolder = Path(Config.getSpoolsFolder(environment))
    scriptToExecute = changesetfiles.split('!')
    directory = DirectoryManager.DirectoryManager(environment)
    directory.getAllFiles(files)
    # Sort files by modified date
    files.sort(key=getPathModifiedDate)
    directory.prepareSpoolPath(files, spoolsFolder)
    db = DbManager.Oracle(environment)
    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            files.remove(file)
    for file in files:
        for scriptName in scriptToExecute:
            if scriptName == file.name:
                queryResult, errorMessage = db.runScriptFiles(file)
                # directory.prepareRunLog(spoolsFolder)
                # directory.writeRunLog(queryResult, errorMessage, file.name, spoolsFolder)

    # Preprod İşlemleri
    if environment == "PREPROD":
        for file in files:
            for scriptName in scriptToExecute:
                if scriptName == file.name:
                    directory.copyScriptToProdDbFolder(file)
        directory.copyDeployPackInfoTo09()

    db.recompileInvalidObjects()
    db.getInvalidObjects(spoolsFolder)
    invalidObjectListFile = File.File(
        "InvalidObjects.log", spoolsFolder / "InvalidObjects.log")
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
    if Config.isRequiredUserLogin() == "TRUE":
        Auth.logoffUser()
    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            continue
        if file.name.upper() == directory.runLog.upper():
            continue
        for scriptName in scriptToExecute:
            if scriptName == file.name:
                directory.removeSpool(file)
    directory.removeSpool(invalidObjectListFile)
    
    return jsonify({'result': 'OK'})


@app.route('/print/<string:files>', methods=['GET'])
def p(files):
    fileList = files.split('!')
    for f in fileList:
        print(f)
    return jsonify({'result': 'OK'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
