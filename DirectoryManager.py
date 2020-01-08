from pathlib import Path
import os
import datetime
import File
import Config
import shutil
import ExceptionManager

exceptionFileName = "Directory.py"


class DirectoryManager:

    def __init__(self, environment):
        self.deployPackInfo = 'DeployPackInfo.log'
        self.runLog = 'Run.log'
        self.preparePaths(environment)

    def preparePaths(self, environment):
        # Root Path
        self.scriptFolder = Path(self.getScriptFolderDirectory(environment))
        # Old klasör yapısı
        self.OldFolder = self.getOldFolderDirectory(environment)

        # Preprod
        self.env = environment
        if self.env.upper() == 'PREPROD':
            self.prodDbDeployPath = self.getProdDbDeployPath()
            self.packInfoFromDbFolder = self.OldFolder / self.deployPackInfo
            self.packInfoFromProdDbDeploy = self.prodDbDeployPath / self.deployPackInfo

    @staticmethod
    def getDateWithTime():
        return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    def createDirectory(self, path):
        try:
            if not Path.exists(path):
                Path(path).mkdir()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "createDirectory", exceptionFileName)

    def move(self, source, destination):
        try:
            shutil.move(str(source.resolve()),
                        str(destination.resolve()))
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "move", exceptionFileName)

    def getScriptFolderDirectory(self, environment):
        return Path(Config.getScriptFolderDirectory(environment))

    def getOldFolderDirectory(self, environment):
        oldDirectory = Path(Config.getOldFolderDirectory(environment))
        oldDirectory = oldDirectory / self.getDateWithTime()
        return oldDirectory

    def getAllFiles(self, files):
        for (l_dirpath, l_dirnames, l_filenames) in os.walk(self.scriptFolder):
            if l_filenames:
                for fileName in l_filenames:
                    filePath = Path(Path(l_dirpath).resolve(), fileName)
                    files.append(File.File(fileName, filePath))

    def moveScriptsToOldFolder(self, files):
        for file in files:
            self.move(file.path, self.OldFolder)
            file.path = self.OldFolder.resolve() / file.name

    def prepareSpoolPath(self, files, target):
        for file in files:
            file.spoolPath = Path(target) / file.name
            file.spoolPath = file.spoolPath.with_suffix('.log')

    def prepareRunLog(self, target):
        try:
            with open(target.resolve() / self.runLog, "a+") as f:
                f.write("Versiyon: 0.2.5")
            f.close()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "writeRunLog", exceptionFileName)

    def writeRunLog(self, queryResult, errorMessage, fileName, target):
        try:
            with open(target.resolve() / self.runLog, "a+") as f:
                f.write("\n")
                f.write("-----------------\n")
                f.write(fileName + " - " + str(queryResult))
            f.close()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "writeRunLog", exceptionFileName)

    # PreProd
    def getProdDbDeployPath(self):
        return Path(Config.getProdDbDeployPath(self.env))

    def copyScriptToProdDbFolder(self, file):
        self.copy(file.path, self.prodDbDeployPath)
        file.path = self.prodDbDeployPath.resolve() / file.name

    def copyDeployPackInfoTo09(self):
        self.copy(self.scriptFolder / self.deployPackInfo, self.prodDbDeployPath)

    def copy(self, source, destination):
        try:
            shutil.copy(str(source.resolve()),
                        str(destination.resolve()))
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "copy", exceptionFileName)

    def removeSpool(self, file):
        self.remove(file.spoolPath)

    def remove(self, path):
        try:
            os.remove(path)
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "remove", exceptionFileName)

    def readDeployPackInfo(self):
        read_data = ''
        try:
            with open(self.packInfoFromDbFolder.resolve()) as f:
                read_data = f.read()
            f.close()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "readDeployPackInfo", exceptionFileName)
        return read_data

    def appendDeployPackInfoTo09(self, content):
        try:
            with open(self.packInfoFromProdDbDeploy.resolve(), 'a+') as f:
                f.write('\n')
                f.write(content)
            f.close()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "appendDeployPackInfoTo09", exceptionFileName)
