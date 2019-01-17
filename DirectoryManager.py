from pathlib import Path
import os
import datetime
import File
import Config
import shutil
import ExceptionManager

exceptionFileName = "Directory.py"


class DirectoryManager:

    def __init__(self, environtment):
        self.deployPackInfo = 'DeployPackInfo.log'
        self.runLog = 'Run.log'
        # Root Path
        self.rootPath = Path(self.getRootDirectory())
        # Old klasör yapısı
        self.OldRootDir = self.getOldRootDirectory()
        
        # Preprod
        self.env = environtment
        if self.env.upper() == 'PREPROD':
            self.prodDbDeployPath = self.getProdDbDeployPath()
            self.packInfoFromDbFolder = self.OldRootDir / self.deployPackInfo
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

    def getRootDirectory(self):
        return Path(Config.getRootDirectory())

    def getOldRootDirectory(self):
        oldDirectory = Path(Config.getOldDirectory())
        oldDirectory = oldDirectory / self.getDateWithTime()
        return oldDirectory

    def getAllFiles(self, files):
        for (l_dirpath, l_dirnames, l_filenames) in os.walk(self.rootPath):
            if l_filenames:
                for fileName in l_filenames:
                    filePath = Path(Path(l_dirpath).resolve(), fileName)
                    files.append(File.File(fileName, filePath))

    def moveScriptsToOldFolder(self, files):
        for file in files:
            self.move(file.path, self.OldRootDir)
            file.path = self.OldRootDir.resolve() / file.name

    def prepareSpoolPath(self, files):
        for file in files:
            file.spoolPath = file.path.with_suffix('.log')

    def prepareRunLog(self):
        try:
            with open(self.OldRootDir.resolve() / self.runLog, "a+") as f:
                f.write("Versiyon: 0.2.1")
            f.close()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "writeRunLog", exceptionFileName)

    def writeRunLog(self, queryResult, errorMessage, fileName):
        try:
            with open(self.OldRootDir.resolve() / self.runLog, "a+") as f:
                f.write("\n")
                f.write("-----------------\n")
                f.write(fileName + " - " + str(queryResult))
            f.close()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "writeRunLog", exceptionFileName)

    # PreProd
    def getProdDbDeployPath(self):
        return Path(Config.getProdDbDeployPath())

    def copyScriptToProdDbFolder(self, file):
        self.copy(file.path, self.prodDbDeployPath)
        file.path = self.prodDbDeployPath.resolve() / file.name
    
    def copyDeployPackInfoTo09(self):
        self.copy(self.rootPath / self.deployPackInfo, self.prodDbDeployPath)

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
