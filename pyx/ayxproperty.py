from typing import Dict
from decorators import newobj

class InvalidAttributeNameError(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

        super(InvalidAttributeNameError, self).__init__('message: {}, errors: {}'.format(message, errors))

    def __reduce__(self):
        return (InvalidAttributeNameError, (self.message, self.errors))

class AyxProperty:
    """
    Represents a property field in an Alteryx workflow or tool configuration.
    """
    def __init__(self, name: str, value: str = ""):
        self.name: str = name
        self.value: str = value
        self.attributes: Dict[str, str] = dict({})

    @newobj
    def set_attribute(self, key: str, value: str) -> '__class__':
        self.attributes[key] = value

    @newobj
    def set_attributes(self, attributes: Dict[str, str]) -> '__class__':
        self.attributes += attributes

    def get_attribute(self, key: str) -> str:
        if key in self.attributes:
            return self.attributes[key]
        else:
            raise InvalidAttributeNameError('Attribute "{}" does not exist'.format(key), "")

    def get_attributes(self) -> Dict[str, str]:
        return self.attributes
