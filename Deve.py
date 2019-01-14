import sys
from pathlib import Path
import File
import DirectoryManager
import SqlPlus
import Config
import Email
"""
Oracle script çalıştırma uygulaması
"""
if __name__ == "__main__":
    print("###### Deve #####")
    env = Config.getEnvironment()
    print(env + " Deploy Started!")
    files = []
    directory = DirectoryManager.DirectoryManager(env)
    print("## Reading files")
    directory.getAllFiles(files)
    print("## Moving files to Old Folder")
    directory.moveScriptsToOldFolder(files)
    directory.prepareSpoolPath(files)
    db = SqlPlus.Oracle()
    for file in files:
        if file.name.upper() == directory.deployPackInfo.upper():
            continue
        print("Executing File: ", file.name)
        queryResult, errorMessage = db.runScriptFiles(file)
        directory.prepareRunLog()
        directory.writeRunLog(queryResult, errorMessage, file.name)

    if env.upper() == 'PREPROD':
        print("## Files are copying to '9_ProdDbDeploy' Folder")
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
    x = input("Please, press enter to finish...")
