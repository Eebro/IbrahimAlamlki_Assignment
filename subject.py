from typing import List
from enums import RoleType

# Define the Subject class to represent a user subject
class Subject:
    def __init__(self, name: str, roles: List[RoleType], salt: str, salted_hash: str):
        self.name = name
        self.roles = roles
        self.salt = salt
        self.salted_hash = salted_hash

    def get_name(self) -> str:
        # Get the name of the subject
        return self.name

    def get_roles(self) -> List[RoleType]:
        # Get the roles associated with the subject
        return [RoleType[r] for r in self.roles]

    def get_salt(self) -> str:
        # Get the salt associated with the subject's password
        return self.salt

    def get_salted_hash(self) -> str:
        # Get the salted hash of the subject's password
        return self.salted_hash
