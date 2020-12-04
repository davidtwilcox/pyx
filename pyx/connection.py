# Pyx, a Python module for creating, reading, and editing Alteryx Designer workflows entirely in code
# Copyright (C) 2020  David T. Wilcox

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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