from access_control import AccessControl
from enroller import Enroller

class EnrollerTest:

    def __init__(self):
        ac = AccessControl()
        self.e = Enroller(ac)

    def test_password_mechanism(self, username, password, roles):
        self.e.save_record(username, password, roles)
        ac = AccessControl()
        s = ac.get_user(username)
        if s is not None:
            print(f"{username} was added to the password file successfully.")
        else:
            print(f"Failed to add the following user to the password file: {username}")

    def test_password_checker(self, password, username, expected):
        actual = self.e.password_checker(password, username) is None
        print(f"Is password valid for password '{password}' and username '{username}'? Expected: {expected}. Actual: {actual}")

if __name__ == "__main__":
    username = "NickPerez"
    password = "vAlidPass!"
    roles = [1]  # 1 corresponds to premium client.

    test = EnrollerTest()
    test.test_password_mechanism(username, password, roles)

    test.test_password_checker("password", "password", False)  # same as username
    test.test_password_checker("password", "hello", False)  # common password
    test.test_password_checker("passwoRd!", "password", False)  # missing digit
    test.test_password_checker("pass*word3", "password", False)  # missing uppercase
    test.test_password_checker("PASSWORD%H2", "password", False)  # missing lowercase
    test.test_password_checker("pasS4word", "password", False)  # missing special character
    test.test_password_checker("6137231234", "password", False)  # follows common format (phone num)
    test.test_password_checker("Passw0rd!", "password", True)  # valid
