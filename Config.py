import configparser
import ExceptionManager

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
        exit()


def getOldDirectory():
    try:
        return config['DIRECTORY']['OLDDIR']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getOldDirectory", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        exit()


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
        exit()
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
        exit()


def getMailFrom():
    try:
        return config['MAIL']['FROM']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailFrom", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        exit()


def getMailTo():
    try:
        return config['MAIL']['FROM']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailTo", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        exit()


def getMailPassword():
    try:
        return config['MAIL']['PASSWORD']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getMailPassword", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        exit()


def getEnvironment():
    try:
        return config['APP']['ENVIRONMENT']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getEnvironment", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        exit()

# Preprod


def getProdDbDeployPath():
    try:
        return config['DIRECTORY']['PRODDBDEPLOY']
    except Exception as error:
        ExceptionManager.WriteException(
            str(error), "getProdDbDeployPath", exceptionFileName)
        print(error)
        x = input("Press enter to finish...")
        exit()
