from typing import List
from access_control import AccessControl
from enroller import Enroller
from login import LogIn

class LogInTest:

    def __init__(self):
        ac = AccessControl()
        self.e = Enroller(ac)
        self.l = LogIn(ac)

    def test_enrollment_login(self, username: str, password: str, roles: List[int]):
        self.e.save_record(username, password, roles)  # save record
        login_result = self.l.process_login(username, password)
        if not login_result:
            print("Enrollment and login mechanism failed")
        else:
            print("Enrollment and login mechanism successful")

if __name__ == "__main__":
    username = "VelmaMac"
    password = "vAlidPass!"
    roles = [0]  # 1 corresponds to regular client

    test = LogInTest()
    test.test_enrollment_login(username, password, roles)
