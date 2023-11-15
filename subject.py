from typing import List
from enums import RoleType

class Subject:
    def __init__(self, name: str, roles: List[RoleType], salt: str, salted_hash: str):
        self.name = name
        self.roles = roles
        self.salt = salt
        self.salted_hash = salted_hash

    def get_name(self) -> str:
        return self.name

    def get_roles(self):
        return [RoleType[r] for r in self.roles]

    def get_salt(self) -> str:
        return self.salt

    def get_salted_hash(self) -> str:
        return self.salted_hash
