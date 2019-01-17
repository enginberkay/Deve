import configparser
import ExceptionManager
import os

config = configparser.ConfigParser()
config.read('config.ini')
exceptionFileName = "Config.py"


def getRootDirectory():
    try:
        return config['DIRECTORY']['ROOTDIR']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getRootDirectory", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)


def getOldDirectory():
    try:
        return config['DIRECTORY']['OLDDIR']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getOldDirectory", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)


def getDbConnectionString():
    try:
        userName = config['DATABASE']['USERNAME']
        password = config['DATABASE']['PASSWORD']
        tnsName = config['DATABASE']['TNSNAME']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getDbConnectionString", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)
    return str(userName + "/" + password + "@" + tnsName)

# Mail


def getMailActive():
    try:
        return config['MAIL']['ACTIVE']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailRequired", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)


def getMailFrom():
    try:
        return config['MAIL']['FROM']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailFrom", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)


def getMailTo():
    try:
        return config['MAIL']['FROM']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailTo", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)


def getMailPassword():
    try:
        return config['MAIL']['PASSWORD']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailPassword", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)


def getEnvironment():
    try:
        return config['APP']['ENVIRONMENT']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getEnvironment", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)

def getWindowsUserDomain():
    try:
        return config['AUTHENTICATION']['DOMAIN']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getWindowsUserDomain", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)

def isRequiredUserLogin():
    try:
        return config['AUTHENTICATION']['IS_REQUIRED']
    except Exception as error:
        print("User Login is not required!")
        return "FALSE"

def getWindowsUserName():
    try:
        return config['AUTHENTICATION']['USERNAME']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getWindowsUserName", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)

def getWindowsUserPassword():
    try:
        return config['AUTHENTICATION']['PASSWORD']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getWindowsUserPassword", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)

# Preprod


def getProdDbDeployPath():
    try:
        return config['DIRECTORY']['PRODDBDEPLOY']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getProdDbDeployPath", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        os._exit(1)
