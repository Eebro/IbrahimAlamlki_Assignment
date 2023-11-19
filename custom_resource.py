from enums import ResourceType, AccessType

# Define the Resource class
class Resource:
    def __init__(self, resource_type: ResourceType, access_type: AccessType):
        # Initialize a Resource with a specific resource type and access type
        self.resource_type = resource_type
        self.access_type = access_type

    def get_resource_type(self) -> ResourceType:
        # Get the resource type of the Resource instance
        return self.resource_type

    def get_access_type(self) -> AccessType:
        # Get the access type of the Resource instance
        return self.access_type

    def __str__(self) -> str:
        # String representation of the Resource instance
        return f"User has {self.access_type.name} access to {self.resource_type.name} resource."
