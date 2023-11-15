from enum import Enum

class AccessType(Enum):
    VIEW = 1
    MODIFY = 2
    VALIDATE = 3
    CONDITIONAL = 4