from enums import ResourceType, AccessType

class Resource:
    def __init__(self, resource_type: ResourceType, access_type: AccessType):
        self.resource_type = resource_type
        self.access_type = access_type

    def get_resource_type(self) -> ResourceType:
        return self.resource_type

    def get_access_type(self) -> AccessType:
        return self.access_type

    def __str__(self) -> str:
        return f"User has {self.access_type.name} access to {self.resource_type.name} resource."
