from enums import RoleType, AccessType, ResourceType
from subject import Subject
from role import Role
from custom_resource import Resource
from environment import Environment

class AccessControl:
    NUM_ROLES = len(RoleType)

    PASSWORDS_FILENAME = "passwd.txt"

    def __init__(self):
        self.cap_list = {}
        self.users = {}
        self.user_role_mapping = {}
        self.client_permission = True
        self.validation_required = False
        self.num_users = 0
        self.create_roles()

    def create_roles(self):
        for role_type in RoleType:
            self.cap_list[role_type] = Role.create_capability_list(role_type)

    def get_role_cap_list(self, role_type):
        return self.cap_list.get(role_type, [])

    def get_users(self):
        self.user_role_mapping = {}

        try:
            with open(self.PASSWORDS_FILENAME, 'r') as file:
                for line in file:
                    fields = line.strip().split(':')
                    user_id, salt, salted_hash, roles_str = fields[0], fields[1], fields[2], fields[3]
                    roles = [RoleType.valueOf(role) for role in roles_str.split(',')]

                    role_list = roles
                    user = Subject(user_id, roles, salt, salted_hash)

                    self.users[user_id] = user
                    self.user_role_mapping[user_id] = role_list

        except FileNotFoundError as e:
            print("An error occurred while processing the common passwords file.")
            print(e)

    def add_user(self, subject):
        self.users[subject.get_name()] = subject

    def get_user(self, user_id):
        return self.users.get(user_id)

    def check_environment_attributes(self, role_type):
        if role_type == RoleType.TELLER and not Environment.get_curr_hour() <= 17 and Environment.get_curr_hour() >= 9:
            return False

        return True

    def does_username_already_exist(self, username):
        return username in self.users

    def check_access(self, role_type, access_type, resource_type):
        if role_type == RoleType.TELLER and not self.check_environment_attributes(role_type):
            return False

        if role_type == RoleType.TECH_SUPPORT and not self.client_permission:
            return False

        if role_type == RoleType.COMPLIANCE_OFFICER and not self.validation_required:
            return False

        for resource in self.cap_list.get(role_type, []):
            if resource.get_resource_type() == resource_type:
                if (
                    resource.get_access_type() == access_type
                    or (resource.get_access_type() == AccessType.MODIFY and access_type == AccessType.VIEW)
                ):
                    return True

        return False

if __name__ == "__main__":
    # You can add your main method or any testing code here
    pass