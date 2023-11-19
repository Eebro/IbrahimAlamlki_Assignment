from enums import RoleType, AccessType, ResourceType
from subject import Subject
from role import Role
from custom_resource import Resource
from environment import Environment

# Define the AccessControl class
class AccessControl:
    NUM_ROLES = len(RoleType)
    PASSWORDS_FILENAME = "passwd.txt"

    def __init__(self):
        self.cap_list = {}  # Capability list for each role
        self.users = self.get_users()  # Dictionary to store user information
        self.user_role_mapping = {}  # Mapping of user IDs to their roles
        self.client_permission = True  # Client permission flag
        self.validation_required = False  # Validation requirement flag
        self.num_users = 0  # Number of users
        self.create_roles()  # Initialize role capabilities

    def create_roles(self):
        # Create capability lists for each role
        for role_type in RoleType:
            self.cap_list[role_type] = Role.create_capability_list(role_type)

    def get_role_cap_list(self, role_type):
        # Retrieve capability list for a given role
        return self.cap_list.get(role_type, [])

    def get_users(self):
        # Populate user information from a passwords file
        self.user_role_mapping = {}
        users = {}  # Initialize an empty dictionary to store users

        try:
            with open(self.PASSWORDS_FILENAME, 'r') as file:
                for line in file:
                    fields = line.strip().split(':')  # Using colon (:) as the delimiter
                    user_id, salt, salted_hash, roles_str = fields[0], fields[1], fields[2], fields[3]
                    roles = roles_str.split(',')

                    role_list = roles
                    user = Subject(user_id, roles, salt, salted_hash)

                    users[user_id] = user
                    self.user_role_mapping[user_id] = role_list

        except FileNotFoundError as e:
            print("An error occurred while processing the common passwords file.")
            print(e)

        return users  # Return the populated users dictionary

    def add_user(self, subject):
        # Add a new user to the system
        if isinstance(subject, Subject):
            self.users[subject.get_name()] = subject
        else:
            raise ValueError("Invalid subject type. Must be an instance of the Subject class.")

    def get_user(self, user_id):
        # Retrieve a user by user ID
        # Directly return the user if it exists, otherwise return None
        return self.users.get(user_id, None)

    def check_environment_attributes(self, role_type):
        # Check environmental attributes for specific roles
        if role_type == RoleType.TELLER and not Environment.get_curr_hour() <= 23 and Environment.get_curr_hour() >= 9:
            return False

        return True

    def does_username_already_exist(self, username):
        # Check if a username already exists in the system
        return username in self.users

    def check_access(self, role_type, access_type, resource_type):
        # Check if a role has access to a specific resource with the given access type
        if role_type == RoleType.TELLER and not self.check_environment_attributes(role_type):
            return False

        if role_type == RoleType.TECH_SUPPORT and not self.client_permission:
            return False

        if role_type == RoleType.COMPLIANCE_OFFICER and not self.validation_required:
            return False

        for role_resource in self.cap_list.get(role_type, []):
            if isinstance(role_resource, Resource) and role_resource.get_resource_type() == resource_type:
                if (
                    role_resource.get_access_type() == access_type
                    or (role_resource.get_access_type() == AccessType.MODIFY and access_type == AccessType.VIEW)
                ):
                    return True

        return False

if __name__ == "__main__":
    ac = AccessControl()
    
    # Retrieve users and print their information
    users = ac.get_users()
    for user_id, user in users.items():
        print(f"User ID: {user_id}, Roles: {user.get_roles()}")
