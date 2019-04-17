import configparser
import ExceptionManager
import os
import sys

config = configparser.ConfigParser()
config.read('config.ini')
exceptionFileName = "Config.py"


class Config:
    
    def __init__(self, args):
        self.environment=None
        self.ScriptsFolder=None
        self.OldFolderDir=None
        self.DbConnectionStr=None
        self.ProdDbDeployPath=None
        if args!=None:
            self.environment=args[1]
            self.ScriptsFolder=args[2]
            self.OldFolderDir=args[3]
            self.DbConnectionStr=args[4]
            self.ProdDbDeployPath=args[5]  
        
    def getEnvironment(self):
        try:
            if self.environment!=None:
                return self.environment
            else:
                return config['APP']['ENVIRONMENT']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getEnvironment", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getScriptFolderDirectory(self, environment):
        try:
            if self.ScriptsFolder!=None:
                return self.ScriptsFolder
            elif environment == 'TEST':
                return config['DIRECTORY_TEST']['SCRIPT_FOLDER']
            elif environment == 'PREPROD':
                return config['DIRECTORY_PREPROD']['SCRIPT_FOLDER']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getRootDirectory", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getOldFolderDirectory(self, environment):
        try:
            if self.OldFolderDir!=None:
                return self.OldFolderDir
            elif environment == 'TEST':
                return config['DIRECTORY_TEST']['OLD_FOLDER_DIR']
            elif environment == 'PREPROD':
                return config['DIRECTORY_PREPROD']['OLD_FOLDER_DIR']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getOldDirectory", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getDbConnectionString(self, environment):
        try:
            
            if self.DbConnectionStr!=None:
                return self.DbConnectionStr
            elif environment == 'TEST':
                userName = config['DATABASE_TEST']['USERNAME']
                password = config['DATABASE_TEST']['PASSWORD']
                tnsName = config['DATABASE_TEST']['TNSNAME']
            elif environment == 'PREPROD':
                userName = config['DATABASE_PREPROD']['USERNAME']
                password = config['DATABASE_PREPROD']['PASSWORD']
                tnsName = config['DATABASE_PREPROD']['TNSNAME']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getDbConnectionString", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)
        return str(userName + "/" + password + "@" + tnsName)


    # Preprod


    def getProdDbDeployPath(self):
        try:
            if self.ProdDbDeployPath!=None:
                return self.ProdDbDeployPath
            else:
                return config['DIRECTORY_PREPROD']['PRODDBDEPLOY']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getProdDbDeployPath", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)
    # VZX


    def getSpoolsFolder(self, environment):
        try:
            if environment == 'TEST':
                return config['DIRECTORY_TEST']['SPOOLS']
            elif environment == 'PREPROD':
                return config['DIRECTORY_PREPROD']['SPOOLS']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getProdDbDeployPath", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)

    # Mail


    def getMailActive(self):
        try:
            return config['MAIL']['ACTIVE']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getMailRequired", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getMailFrom(self):
        try:
            return config['MAIL']['FROM']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getMailFrom", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getMailTo(self):
        try:
            return config['MAIL']['FROM']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getMailTo", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getMailPassword(self):
        try:
            return config['MAIL']['PASSWORD']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getMailPassword", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    #authentication

    def getWindowsUserDomain(self):
        try:
            return config['AUTHENTICATION']['DOMAIN']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getWindowsUserDomain", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def isRequiredUserLogin(self):
        try:
            return config['AUTHENTICATION']['IS_REQUIRED']
        except Exception as error:
            print("User Login is not required!")
            return "FALSE"


    def getWindowsUserName(self):
        try:
            return config['AUTHENTICATION']['USERNAME']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getWindowsUserName", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)


    def getWindowsUserPassword(self):
        try:
            return config['AUTHENTICATION']['PASSWORD']
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "getWindowsUserPassword", exceptionFileName)
            print(error)
            x = input("Press enter to finish...")
            os._exit(1)
