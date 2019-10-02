import win32security
import win32con
import Config
import ExceptionManager

exceptionFileName = "AuthenticationManager.py"


class AccountImpersonate:

    def __init__(self):
        self.domain = Config.getWindowsUserDomain()
        self.username = Config.getWindowsUserName()
        self.password = Config.getWindowsUserPassword()

    def logonUser(self):
        try:
            self.handel = win32security.LogonUser(
                self.username, self.domain, self.password, win32con.LOGON32_LOGON_INTERACTIVE, win32con.LOGON32_PROVIDER_DEFAULT)
            win32security.ImpersonateLoggedOnUser(self.handel)
            return True
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "logonUser", exceptionFileName)
            return False

    def logoffUser(self):
        try:
            win32security.RevertToSelf()
            self.handel.Close()
            return True
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "logoffUser", exceptionFileName)
            return False
