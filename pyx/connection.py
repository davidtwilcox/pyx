from .tool import Tool
import xml.etree.ElementTree as ET
from dataclasses import dataclass


@dataclass
class Connection:
    """
    Represents a connection between two tools.
    """
    origin_tool_id: int = 0
    origin_output: str = ''
    destination_tool_id: int = 0
    destination_input: str = ''

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the connection.
        """
        # Dummy element that ElementTree extend() will strip
        root = ET.Element('root')

        connection = ET.SubElement(root, 'Connection')

        origin = ET.SubElement(connection, 'Origin')
        origin.set('ToolID', str(self.origin_tool_id))
        origin.set('Connection', self.origin_output)

        destination = ET.SubElement(connection, 'Destination')
        destination.set('ToolID', str(self.destination_tool_id))
        destination.set('Connection', self.destination_input)

        return root