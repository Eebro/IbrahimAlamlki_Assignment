import re
import hashlib
import os
from access_control import AccessControl
from enums import RoleType
from subject import Subject

# Define the Enroller class for user enrollment
class Enroller:

    def __init__(self, ac: AccessControl):
        self.ac = ac
        self.reader = input
        self.common_passwords = self.get_common_passwords()

    def get_common_passwords(self):
        # Retrieve common passwords from a file
        common_passwords = []
        try:
            with open("commonPasswords.txt", "r") as f:
                common_passwords = [line.strip().lower() for line in f.readlines()]
        except FileNotFoundError:
            print("An error occurred while processing the common passwords file.")
        return common_passwords
    
    @staticmethod
    def hash_password(password, salt):
        # Hash the password using SHA-256 with a provided salt
        sha256 = hashlib.sha256()
        sha256.update(salt)
        sha256.update(password.encode('utf-8'))
        return sha256.digest()

    def enrol_user(self):
        print("Finvest Holdings Registration")
        print ("Client Holdings and Information System\n------------------------------------------")
        
        username = self.get_unique_username()
        password = self.get_valid_password(username)
        roles = self.get_roles()
        self.save_record(username, password, roles)

    def get_unique_username(self):
        # Prompt the user for a unique username
        username = self.reader("Enter a Username: ")
        while self.ac.does_username_already_exist(username):
            print("Sorry, that username already exists. Choose another one.")
            username = self.reader("Username: ")
        return username

    def print_password_policy(self):
        # Display the password policy to the user
        print("\nEnter a Password...")
        print("Password must be 8-12 characters in length.")
        print("Password must include at least:\n\t- one upper-case letter\n\t- one lower-case letter\n\t- one numerical digit, and\n\t- one special character from the set {!,@,#,$,%,?,*}")
        print("Password can not be found on a list of common weak passwords (ex. password, qwerty123, etc.).")
        print("Password can not match the format of calendar dates, license plate numbers, telephone numbers, or other common numbers.")
        print("Password can not match your username.")

    def get_valid_password(self, username):
        # Prompt the user for a valid password based on the password policy
        self.print_password_policy()
        password = self.reader("\nPassword: ")
        pwd_check = self.password_checker(password, username)
        while pwd_check:
            print(f"{pwd_check} Please try again.")
            password = self.reader("Password: ")
            pwd_check = self.password_checker(password, username)
        return password

    def password_checker(self, password, username):
        # Check if the provided password meets the specified criteria
        if password == username:
            return "Password cannot match the username."

        if password.lower() in self.common_passwords:
            return "This password is too common."

        common_formats = [
            r'^\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})$',  # phone number
            r'^(?!.*[DFIOQU])[A-VXY][0-9][A-Z] ?[0-9][A-Z][0-9]$',  # Canadian postal code
            r'^[A-Z]{3,4}\d{1,4}$',  # license plate
            r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$',  # dd-mm-yyyy format
            r'^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$',  # mm/dd/yyyy format
            r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$',  # yyyy-mm-dd format
            r'^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[012])(19|20)\d\d$'  # ddmmyyyy
        ]

        for regex in common_formats:
            if re.match(regex, password):
                return "Password format is not allowed."

        if not 8 <= len(password) <= 12:
            return "Password must be between 8-12 characters in length."

        if not any(char.isdigit() for char in password):
            return "Password must contain a digit."

        if not any(char.islower() for char in password):
            return "Password must contain a lowercase letter."

        if not any(char.isupper() for char in password):
            return "Password must contain an uppercase letter."

        if not any(char in r'!@#$%?*' for char in password):
            return "Password must contain a special character."

        return None

    def get_roles(self):
        # Prompt the user to select roles from available options
        print("Enter the number corresponding to the role of the user. The available roles are: ")
        for i, r in enumerate(RoleType):
            print(f"{i} - {r.name}")  # Access the name attribute to get the enum member without the enum type
        roles = []
        cont = True
        while cont:
            try:
                role = int(self.reader("\nRole Number: "))
                if 0 <= role < len(RoleType):
                    roles.append(role)
                    cont = self.reader("\nWould you like to add another role to this user (Y/n)? ").lower() != "n"
                else:
                    print("Invalid role. Try again.")
            except ValueError:
                print("Invalid role. Try again.")
        return roles

    def save_record(self, username, password, roles):
        # Save the user record with hashed password and roles information
        role_types = [  "PREMIUM_CLIENT", "FINANCIAL_ADVISOR", "FINANCIAL_PLANNER","TELLER","INVESTMENT_ANALYST","COMPLIANCE_OFFICER","TECH_SUPPORT"]
        roles = [role - 1 for role in roles]

        roles_list = [role_types[role] for role in roles]
        salt = os.urandom(16)
        hashed_password = self.hash_password(password, salt)

        record = f"{username}:{self.bytes_to_hex(salt)}:{self.bytes_to_hex(hashed_password)}:{','.join(map(str, roles_list))}\n"

        with open(AccessControl.PASSWORDS_FILENAME, "a") as file:
            file.write(record)

        new_subject = Subject(username, roles_list, self.bytes_to_hex(salt), self.bytes_to_hex(hashed_password))
        self.ac.add_user(new_subject)

        print("Added the following record:\n" + record)

    @staticmethod
    def bytes_to_hex(data):
        # Convert bytes to hexadecimal string
        return data.hex()

if __name__ == "__main__":
    # Create an instance of AccessControl and Enroller, then enroll a user
    ac = AccessControl()
    eu = Enroller(ac)
    eu.enrol_user()
