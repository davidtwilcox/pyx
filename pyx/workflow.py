import os
import subprocess
import xml.etree.ElementTree as ET
from typing import Dict, OrderedDict, List, Any
from xml.dom import minidom
import xmltodict

from .connection import Connection
from .decorators import newobj
from .tool import Tool, ToolPosition
from .tool_factory import ToolFactory


class Workflow:
    """
    Contains operations to create, modify, read, and write Alteryx workflows.
    """

    def __init__(self):
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
        self._name: str = ''
        self._filename: str = ''
        self._yxmd_version: str = ''
        self._tools: Dict[int, Tool] = dict({})
        self._connections: List[Connection] = list()
        self._properties: OrderedDict[Any, Any] = dict({})

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        self._filename = value

    @property
    def yxmd_version(self) -> str:
        return self._yxmd_version

    @yxmd_version.setter
    def yxmd_version(self, value: str) -> None:
        self._yxmd_version = value

    @property
    def tools(self) -> Dict[int, Tool]:
        return self._tools

    @tools.setter
    def tools(self, value: Dict[int, Tool]) -> None:
        self._tools = value

    @property
    def connections(self) -> List[Connection]:
        return self._connections

    @connections.setter
    def connections(self, value: List[Connection]) -> None:
        self._connections = value

    @property
    def properties(self) -> OrderedDict[Any, Any]:
        return self._properties

    @properties.setter
    def properties(self, value: OrderedDict[Any, Any]) -> None:
        self._properties = value

    @newobj
    def add_tool(self, tool: Tool) -> '__class__':
        """Adds the provided Tool instance to the workflow.

        If a tool with the same ID exists in the workflow, the provided tool will replace it.
        """
        self.tools[tool.tool_id] = tool

    @newobj
    def remove_tool(self, tool_id: int) -> '__class__':
        """Removes the tool with the provided ID from the workflow.

        If a tool with the provided ID does not exist in the workflow, no action is taken.
        """
        self.tools.pop(tool_id, None)

    @newobj
    def add_connection(self, origin_tool_id: int, origin_output: str,
                          destination_tool_id: int, destination_input: str) -> '__class__':
        """Adds a connection from the origin tool to the destination tool.
        """
        self.connections.append(Connection(origin_tool_id, origin_output, destination_tool_id, destination_input))

    @newobj
    def remove_connection(self, origin_tool_id: int, origin_output: str,
                          destination_tool_id: int, destination_input: str) -> '__class__':
        """Removes a connection from the workflow.
        """
        for c in self.connections:
            if c.origin_tool_id == origin_tool_id and c.origin_output == origin_output and \
               c.destination_tool_id == destination_tool_id and c.destination_input == destination_input:
                self.connections.remove(c)

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the workflow.
        """
        ayx_doc = ET.Element('AlteryxDocument')
        ayx_doc.set('yxmdVer', self.yxmd_version)

        tools = ET.SubElement(ayx_doc, 'Nodes')
        for _, tool_val in self.tools.items():
            tools.extend(tool_val.toxml())

        connections = ET.SubElement(ayx_doc, 'Connections')
        for connection in self.connections:
            connections.extend(connection.toxml())

        xml: str = xmltodict.unparse({'Root': {'Properties': self.properties}})
        properties: ET.Element = ET.fromstring(xml)
        ayx_doc.extend(properties)

        return ayx_doc

    @staticmethod
    def write(workflow: '__class__', overwrite: bool = True) -> None:
        """Writes the workflow to a file, overwriting an existing file desired.

        If no filename has been set, the workflow name is used. If overwrite
        is True, then any existing file with the same name will be overwritten.
        If overwrite is False and a file exists with the same name, this
        method will raise an exception.
        """
        workflow._set_filename(overwrite)

        pretty_xml = str(workflow)

        with open(workflow.filename, 'w') as f:
            f.write(pretty_xml)

    @staticmethod
    def read(filename: str) -> '__class__':
        """Reads a workflow from the specified file and configures this instance accordingly.
        """
        workflow: Workflow = Workflow()
        with open(filename) as wf:
            xml = xmltodict.parse(wf.read())

            ayx_doc = xml['AlteryxDocument']
            try:
                workflow.name = ayx_doc['Properties']['MetaInfo']['Name']
            except KeyError:
                workflow.name = 'New Workflow'

            workflow.yxmd_version = ayx_doc['@yxmdVer']

            nodes = ayx_doc['Nodes']
            for node in nodes['Node']:
                tool_id: int = int(node['@ToolID'])

                gui_settings = node['GuiSettings']
                plugin = gui_settings['@Plugin']

                tool: Tool = ToolFactory.create_tool(plugin, tool_id)

                position = gui_settings['Position']
                tool.position = ToolPosition(x=int(position['@x']), y=int(position['@y']))

                tool.properties = node['Properties']

                engine_settings = node['EngineSettings']
                tool.engine_dll = engine_settings['@EngineDll']
                tool.engine_dll_entry_point = engine_settings['@EngineDllEntryPoint']

                workflow.add_tool(tool)

            connections = ayx_doc['Connections']
            for connection in connections['Connection']:
                origin = connection['Origin']
                origin_tool_id: int = int(origin['@ToolID'])
                origin_connection: str = origin['@Connection']

                destination = connection['Destination']
                destination_tool_id: int = int(destination['@ToolID'])
                destination_connection: str = destination['@Connection']

                workflow.add_connection(origin_tool_id, origin_connection,
                                    destination_tool_id, destination_connection)

                workflow.tools[origin_tool_id].add_output(destination_tool_id,
                                                          origin_connection,
                                                          destination_connection)
                workflow.tools[destination_tool_id].add_input(origin_tool_id,
                                                              origin_connection,
                                                              destination_connection)

            workflow.properties = ayx_doc['Properties']

        return workflow

    @staticmethod
    def run(self, executable_path: str, overwrite: bool = True) -> None:
        """Runs the workflow using a locally installed copy of the Alteryx engine.

        If no filename is provided, the workflow name is used. If overwrite
        is True, then any existing file with the same name will be overwritten.
        If overwrite is False and a file exists with the same name, this
        method will raise an exception.
        """
        self._set_filename(overwrite)

        pretty_xml = str(self)

        with open(self.filename, 'w') as f:
            f.write(pretty_xml)

        cmd = f"{executable_path} {self.filename}"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, creationflags=0x08000000)
        process.wait()

    def _set_filename(self, overwrite: bool = True):
        if self.filename == "":
            self.filename = f"{self.name}.yxmd"

        if not overwrite and os.path.isfile(self.filename):
            raise FileExistsError('File "{}" already exists and overwrite is false'.format(self.filename))

    def __repr__(self) -> str:
        xml = self.toxml()
        text = ET.tostring(xml, 'utf-8')
        parsed = minidom.parseString(text)
        return parsed.toprettyxml(indent='  ').replace('&quot;', '"')
