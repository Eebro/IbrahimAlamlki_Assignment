from typing import List
from access_control import AccessControl
from enroller import Enroller
from login import LogIn

# Define a class for testing the enrollment and login mechanism
class LogInTest:

    # Constructor initializes instances of AccessControl, Enroller, and LogIn
    def __init__(self):
        ac = AccessControl()
        self.e = Enroller(ac)  # Create an Enroller instance with AccessControl
        self.l = LogIn(ac)     # Create a LogIn instance with AccessControl

    # Method to test enrollment and login
    def test_enrollment_login(self, username: str, password: str, roles: List[int]):
        self.e.save_record(username, password, roles)  # Save user record
        login_result = self.l.process_login(username, password)  # Attempt login
        if not login_result:
            print("Enrollment and login mechanism failed")
        else:
            print("Enrollment and login mechanism successful")


if __name__ == "__main__":
    # Test data
    username = "VelmaMac"
    password = "vAlidPass!"
    roles = [0]  # 0 corresponds to a regular client role

    # Create an instance of LogInTest
    test = LogInTest()

    # Perform enrollment and login test with the given test data
    test.test_enrollment_login(username, password, roles)
