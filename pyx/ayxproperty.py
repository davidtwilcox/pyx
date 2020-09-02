from .decorators import newobj
from .decorators import newobj
from xml.dom import minidom
from typing import Dict, List
import xml.etree.ElementTree as ET


class InvalidAttributeNameError(Exception):
    def __init__(self, message, errors):
        self.message = message
        self.errors = errors

        super(InvalidAttributeNameError, self).__init__('message: {}, errors: {}'.format(message, errors))

    def __reduce__(self):
        return InvalidAttributeNameError, (self.message, self.errors)


class AyxProperty:
    """
    Represents a property field in an Alteryx workflow or tool configuration.
    """
    def __init__(self, name: str, value: str = ""):
        self.name: str = name
        self.value: str = value
        self.attributes: Dict[str, str] = dict({})
        self.children: List['__class__'] = list()

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

    @newobj
    def add_child(self, child: '__class__') -> '__class__':
        self.children.append(child)

    @newobj
    def add_children(self, children: List['__class__']) -> '__class__':
        self.children += children

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the property.
        """
        # Dummy element that ElementTree extend() will strip
        root = ET.Element('root')

        prop = ET.SubElement(root, self.name)
        for key, val in self.attributes.items():
            prop.set(key, val)
        if self.value != '':
            prop.text = self.value
        
        for child in self.children:
            xml = child.toxml()
            prop.extend(xml)
        
        return root

    def __repr__(self) -> str:
        xml = self.toxml()
        text = ET.tostring(xml, 'utf-8')
        parsed = minidom.parseString(text)
        return parsed.toprettyxml(indent='    ')
