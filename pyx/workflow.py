from ayxproperty import AyxProperty
from tool import Tool
from connection import Connection
from decorators import newobj
from xml.dom import minidom
import xml.etree.ElementTree as ET
import os
from typing import Dict, List

class Workflow:
    """
    Contains operations to create, modify, read, and write Alteryx workflows.
    """
    
    def __init__(self, name: str, yxmd_version: str):
        """Initializes the Workflow instance with a name, yxmd file version, and default properties.

        The name can be an arbitrary string. If no file name is specified when the
        workflow is written, the name will be used as the root of the file name,
        with invalid characters converted to underscores.

        The value of yxmd_version should be the full Alteryx version with which
        the workflow will be compatible. For example '2019.2' or '2018.3'.

        All other properties are set to their default values.

        :param name: name of the workflow
        :type name: str
        :param yxmd_version: version string for the workflow
        :type yxmd_version: str
        :return: no value
        :rtype: none
        """
        self.name = name
        self.yxmd_version: str = yxmd_version
        self.tools: Dict[str, Tool] = dict({})
        self.connections: List[Connection] = list()

    def __set_configuration__(self) -> None:                
        self.properties: Dict[str, AyxProperty] = dict({
            'Memory': AyxProperty('Memory').set_attribute('default', 'True'),
            'GlobalRecordLimit': AyxProperty('GlobalRecordLimit').set_attribute('value', '0'),
            'TempFiles': AyxProperty('TempFiles').set_attribute('default', 'True'),
            'Annotation': AyxProperty('Annotation').set_attribute('on', 'True').set_attribute('includeToolName', 'False'),
            'ConvErrorLimit': AyxProperty('ConvErrorLimit').set_attribute('value', 'False'),
            'ConvErrorLimit_Stop': AyxProperty('ConvErrorLimit_Stop').set_attribute('value', 'False'),
            'CancelOnError': AyxProperty('CancelOnError').set_attribute('value', 'False'),
            'DisableBrowse': AyxProperty('DisableBrowse').set_attribute('value', 'False'),
            'EnablePerformanceProfiling': AyxProperty('EnablePerformanceProfiling').set_attribute('value', 'False'),
            'DisableAllOutput': AyxProperty('DisableAllOutput').set_attribute('value', 'False'),
            'ShowAllMacroMessages': AyxProperty('ShowAllMacroMessages').set_attribute('value', 'False'),
            'ShowConnectionStatusIsOn': AyxProperty('ShowConnectionStatusIsOn').set_attribute('value', 'True'),
            'ShowConnectionStatusOnlyWhenRunning': AyxProperty('ShowConnectionStatusOnlyWhenRunning').set_attribute('value', 'True'),
            'ZoomLevel': AyxProperty('ZoomLevel').set_attribute('value', '0'),
            'LayoutType': AyxProperty('LayoutType', 'Horizontal')
        })

        self.metainfo: Dict[str, AyxProperty] = dict({
            'NameIsFileName': AyxProperty('NameIsFileName').set_attribute('value', 'True'),
            'Name': AyxProperty('Name', self.name),
            'Description': AyxProperty('Description'),
            'RootToolName': AyxProperty('RootToolName'),
            'ToolVersion': AyxProperty('ToolVersion'),
            'ToolInDb': AyxProperty('ToolInDb').set_attribute('value', 'False'),
            'CategoryName': AyxProperty('CategoryName'),
            'SearchTags': AyxProperty('SearchTags'),
            'Author': AyxProperty('Author'),
            'Company': AyxProperty('Company'),
            'Copyright': AyxProperty('Copyright'),
            'DescriptionLink': AyxProperty('DescriptionLink').set_attribute('actual', '').set_attribute('displayed', ''),
            'Example': AyxProperty('Example').add_child(AyxProperty('Description')).add_child(AyxProperty('File'))
        })

    @newobj
    def add_tool(self, tool: Tool) -> '__class__':
        """Adds the provided Tool instance to the workflow
        """
        self.tools[tool.tool_id] = tool

    @newobj
    def add_connection(self, origin: Tool, origin_output: str, destination: Tool, destination_input: str) -> '__class__':
        """Adds a connection from the origin tool to the destination tool.
        """
        self.connections.append(Connection(origin, origin_output, destination, destination_input))

    @newobj
    def write(self, filename: str = "", overwrite: bool = True) -> '__class__':
        """Writes the workflow to the specified file.

        If no filename is provided, the workflow name is used. If overwrite
        is True, then any existing file with the same name will be overwritten.
        If overwrite is False and a file exists with the same name, this
        method will raise an exception.
        """
        if filename == "":
            filename = self.name + '.yxmd'
        
        if not overwrite and os.path.isfile(filename):
            raise FileExistsError('File "{}" already exists and overwrite is false'.format(filename))

        pretty_xml = str(self)

        with open(filename, 'w') as f:
            f.write(pretty_xml)

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the workflow.
        """
        self.__set_configuration__()

        ayx_doc = ET.Element('AlteryxDocument')
        ayx_doc.set('yxmdVer', self.yxmd_version)

        tools = ET.SubElement(ayx_doc, 'Nodes')
        for _, tool_val in self.tools.items():
            tools.extend(tool_val.toxml())
        
        connections = ET.SubElement(ayx_doc, 'Connections')
        for connection in self.connections:
            connections.extend(connection.toxml())

        properties = ET.SubElement(ayx_doc, 'Properties')
        for _, prop_val in self.properties.items():
            xml = prop_val.toxml()
            properties.extend(xml)

        metainfo = ET.SubElement(properties, 'MetaInfo')
        for _, mi_val in self.metainfo.items():
            xml = mi_val.toxml()
            metainfo.extend(xml)

        return ayx_doc

    def __repr__(self) -> str:
        xml = self.toxml()
        text = ET.tostring(xml, 'utf-8')
        parsed = minidom.parseString(text)
        return parsed.toprettyxml(indent='  ')
