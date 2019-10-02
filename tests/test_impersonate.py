import unittest
import AuthenticationManager

class TestLogin(unittest.TestCase):
    def test_login(self):
        imp = AuthenticationManager.AccountImpersonate()
        isOk = imp.logonUser()
        self.assertEqual(True, isOk)