import sys
from pathlib import Path
import File
import DirectoryManager
import DbManager
import Config
import Email
"""
Oracle script çalıştırma uygulaması
"""


def getPathModifiedDate(el):
    return Path(el.path).stat().st_mtime


if __name__ == "__main__":
    print("###### Deve #####")
    env = Config.getEnvironment()
    print(env + " Deploy Started!")
    env = env.upper()
    files = []
    directory = DirectoryManager.DirectoryManager(env)
    directory.createDirectory(directory.OldFolder)
    print("## Reading files")
    directory.getAllFiles(files)
    # Sort files by modified date
    files.sort(key=getPathModifiedDate)
    print("## Moving files to Old Folder")
    directory.moveScriptsToOldFolder(files)
    directory.prepareSpoolPath(files, directory.OldFolder)
    db = DbManager.Oracle(env)
    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            continue
        print("Executing File: ", file.name)
        queryResult, errorMessage = db.runScriptFiles(file)
        directory.prepareRunLog(directory.OldFolder)
        directory.writeRunLog(queryResult, errorMessage, file.name, directory.OldFolder)

    if env.upper() == 'PREPROD':
        print("## Files are copying to '9_ProdDbDeploy' Folder")
        for file in files:
            if file.name.upper() == directory.deployPackInfo.upper():
                continue
            if file.name.upper() == directory.runLog.upper():
                continue
            directory.copyScriptToProdDbFolder(file)
        content = directory.readDeployPackInfo()
        directory.appendDeployPackInfoTo09(content)

    print("Recompile Invalid Objects...")
    db.recompileInvalidObjects()
    db.getInvalidObjects(Path(directory.OldFolder))
    invalidObjectListFile = File.File(
        "InvalidObjects.log", directory.OldFolder / "InvalidObjects.log")
    invalidObjectListFile.spoolPath = invalidObjectListFile.path
    files.append(invalidObjectListFile)

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
    x = input("Please, press enter to finish...")
