from ayxproperty import AyxProperty
from decorators import newobj
from xml.dom import minidom
import xml.etree.ElementTree as ET

class Tool:
    """
    Base class for representing an Alteryx tool (or Node in the workflow XML).
    """

    def __init__(self, tool_id: str, configuration: str = ''):
        self.tool_id: str = tool_id
        self.configuration: str = configuration
        self.pos_x: int = 0
        self.pos_y: int = 0
        self.plugin: str = ''
        self.engine_dll: str = ''
        self.engine_dll_entry_point: str = ''

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the tool.
        """
        # Dummy element that ElementTree extend() will strip
        root = ET.Element('root')

        node = ET.SubElement(root, 'Node')
        node.set('ToolID', self.tool_id)

        guisettings = ET.SubElement(node, 'GuiSettings')
        guisettings.set('Plugin', self.plugin)
        position = ET.SubElement(guisettings, 'Position')
        position.set('x', str(self.pos_x))
        position.set('y', str(self.pos_y))

        return root

    def __repr__(self) -> str:
        xml = self.toxml()
        text = ET.tostring(xml, 'utf-8')
        parsed = minidom.parseString(text)
        return parsed.toprettyxml(indent='    ')
