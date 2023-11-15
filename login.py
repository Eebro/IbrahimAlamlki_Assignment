import hashlib
from typing import List
from access_control import AccessControl
from subject import Subject
from enums import RoleType, AccessType
from role import Role
from custom_resource import Resource
from enroller import Enroller

class LogIn:

    not_found_msg = "This account does not exist in the system"
    success_msg = "ACCESS GRANTED"

    def __init__(self, ac: AccessControl):
        self.ac = ac

    def prompt_login(self):
        print("SecVaults Investments, Inc. Log In \n------------------------------------------")
        username = input("Username: ")
        password = input("Password: ")
        self.process_login(username, password)

    def process_login(self, username: str, password: str) -> bool:
        if not self.ac.does_username_already_exist(username):
            print(self.not_found_msg)
            return False

        s = self.ac.get_user(username)

        salt_hash_calculated = self.calculate_salted_hash(s, password)

        if salt_hash_calculated == s.get_salted_hash():
            if RoleType.TELLER in s.get_roles():
                if not self.ac.check_environment_attributes(RoleType.TELLER):
                    print("ACCESS DENIED")
                    return False

            print(self.success_msg)
            self.print_user_info(s)
            return True
        else:
            print(self.not_found_msg)
            return False

    @staticmethod
    def calculate_salted_hash(s: Subject, password: str) -> str:
        try:
            md = hashlib.sha256()
            md.update(LogIn.hex_to_bytes(s.get_salt()))

            salted_hash_password = md.digest(password.encode())

            return Enroller.bytes_to_hex(salted_hash_password)
        except hashlib.AlgorithmAvailable as e:
            print("An exception occurred while calculating salted hash.")
            print(e)
            return ""

    def print_user_info(self, s: Subject):
        print("User ID is: " + s.get_name())
        roles = s.get_roles()
        for r in roles:
            print("As a " + r.name() + ":")
            resources = self.ac.get_role_cap_list(r)
            for res in resources:
                print(res)
                if res.get_access_type() == AccessType.CONDITIONAL:
                    print(Role.get_env_policy(r))

    @staticmethod
    def hex_to_bytes(s: str) -> List[bytes]:
        len_s = len(s)
        byte_arr = [0] * (len_s // 2)
        for i in range(0, len_s, 2):
            byte_arr[i // 2] = bytes([(int(s[i], 16) << 4) + int(s[i + 1], 16)])
        return byte_arr

    @staticmethod
    def main():
        ac = AccessControl()
        login = LogIn(ac)
        login.prompt_login()

if __name__ == "__main__":
    LogIn.main()
