import win32security
import win32con
import Config
import ExceptionManager

exceptionFileName = "AuthenticationManager.py"


class AccountImpersonate:

    def __init__(self, config):
        self.domain = config.getWindowsUserDomain()
        self.username = config.getWindowsUserName()
        self.password = config.getWindowsUserPassword()

    def logonUser(self):
        try:
            self.handel = win32security.LogonUser(
                self.username, self.domain, self.password, win32con.LOGON32_LOGON_INTERACTIVE, win32con.LOGON32_PROVIDER_DEFAULT)
            win32security.ImpersonateLoggedOnUser(self.handel)
        except Win32Exception as e:
            ExceptionManager.WriteException(
                e.strerror, "logonUser", exceptionFileName)
            exit()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "logonUser", exceptionFileName)

    def logoffUser(self):
        try:
            win32security.RevertToSelf()
            self.handel.Close()
        except Win32Exception as e:
            ExceptionManager.WriteException(
                e.strerror, "logoffUser", exceptionFileName)
            exit()
        except Exception as error:
            ExceptionManager.WriteException(
                str(error), "logoffUser", exceptionFileName)
