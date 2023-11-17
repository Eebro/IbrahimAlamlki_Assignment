import hashlib
from typing import List
from access_control import AccessControl
from subject import Subject
from enums import RoleType, AccessType
from role import Role
from enroller import Enroller

class LogIn:

    not_found_msg = "This account does not exist in the system"
    success_msg = "ACCESS GRANTED"

    def __init__(self, ac: AccessControl):
        self.ac = ac
        self.e = Enroller(self.ac)

    def does_username_already_exist(self, username: str) -> bool:
        with open("passwd.txt", "r") as file:
            for line in file:
                stored_username = line.split(":")[0]
                if stored_username == username:
                    return True
        return False
    
    def prompt_login(self):
        print("Finvest Holdings Registration")
        print ("Client Holdings and Information System\n------------------------------------------")
        username = input("Username: ")
        password = input("Password: ")
        self.process_login(username, password)


    def process_login(self, username: str, password: str) -> bool:
        if not self.does_username_already_exist(username):
            print(self.not_found_msg)
            return False
        
        s =  self.ac.get_user(username)

        if not isinstance(s, Subject):
            raise ValueError("Invalid subject type. Must be an instance of the Subject class.")

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
            md.update(bytes(bytearray(LogIn.hex_to_bytes(s.get_salt()))))  # Convert list to bytes
            md.update(password.encode('utf-8'))

            salted_hash_password = md.digest()

            return Enroller.bytes_to_hex(salted_hash_password)
        except AttributeError as e:
            print("An exception occurred while calculating salted hash.")
            print(e)
            return ""



    def print_user_info(self, s: Subject):
        print("User ID is: " + s.get_name())
        roles = s.get_roles()
        for r in roles:
            print("As a " + r.name + ":")
            resources = self.ac.get_role_cap_list(r)
            for res in resources:
                print(res)
                if res.get_access_type() == AccessType.CONDITIONAL:
                    print(Role.get_env_policy(r))



    @staticmethod
    def hex_to_bytes(s: str) -> bytes:
        try:
            return bytes.fromhex(s)
        except ValueError:
            print("Error converting hex to bytes.")
            return b''


if __name__ == "__main__":
    ac = AccessControl()
    login = LogIn(ac)
    login.prompt_login()
