import configparser
import ExceptionManager
import os

config = configparser.ConfigParser()
config.read('config.ini')
exceptionFileName = "Config.py"


def getScriptFolderDirectory(environment):
    try:
        if environment == 'TEST':
            return config['DIRECTORY_TEST']['SCRIPT_FOLDER']
        elif environment == 'PREPROD':
            return config['DIRECTORY_PREPROD']['SCRIPT_FOLDER']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getRootDirectory", exceptionFileName)
        os._exit(1)


def getOldFolderDirectory(environment):
    try:
        if environment == 'TEST':
            return config['DIRECTORY_TEST']['OLD_FOLDER_DIR']
        elif environment == 'PREPROD':
            return config['DIRECTORY_PREPROD']['OLD_FOLDER_DIR']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getOldDirectory", exceptionFileName)
        os._exit(1)


def getDbConnectionString(environment):
    try:
        if environment == 'TEST':
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
        os._exit(1)
    return str(userName + "/" + password + "@" + tnsName)


# Preprod


def getProdDbDeployPath(environment):
    try:
        if environment == 'TEST':
            return config['DIRECTORY_TEST']['PRODDBDEPLOY']
        elif environment == 'PREPROD':
            return config['DIRECTORY_PREPROD']['PRODDBDEPLOY']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getProdDbDeployPath", exceptionFileName)
        os._exit(1)
# VZX


def getSpoolsFolder(environment):
    try:
        return config['DIRECTORY_PREPROD']['SPOOLS']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getProdDbDeployPath", exceptionFileName)
        os._exit(1)

# Mail


def getMailActive():
    try:
        return config['MAIL']['ACTIVE']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailRequired", exceptionFileName)
        os._exit(1)


def getMailFrom():
    try:
        return config['MAIL']['FROM']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailFrom", exceptionFileName)
        os._exit(1)


def getMailTo():
    try:
        return config['MAIL']['FROM']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailTo", exceptionFileName)
        os._exit(1)


def getMailPassword():
    try:
        return config['MAIL']['PASSWORD']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailPassword", exceptionFileName)
        os._exit(1)


def getEnvironment():
    try:
        return config['APP']['ENVIRONMENT']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getEnvironment", exceptionFileName)
        os._exit(1)


def getWindowsUserDomain():
    try:
        return config['AUTHENTICATION']['DOMAIN']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getWindowsUserDomain", exceptionFileName)
        os._exit(1)


def isRequiredUserLogin():
    try:
        return config['AUTHENTICATION']['IS_REQUIRED']
    except:
        return "FALSE"


def getWindowsUserName():
    try:
        return config['AUTHENTICATION']['USERNAME']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getWindowsUserName", exceptionFileName)
        os._exit(1)


def getWindowsUserPassword():
    try:
        return config['AUTHENTICATION']['PASSWORD']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getWindowsUserPassword", exceptionFileName)
        os._exit(1)

def getTfsUrl():
    try:
        return config['TFS']['URL']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getTfsUrl", exceptionFileName)
        os._exit(1)

def getTfsPat():
    try:
        return config['TFS']['PAT']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getTfsPat", exceptionFileName)
        os._exit(1)