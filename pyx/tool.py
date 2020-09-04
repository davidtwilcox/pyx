import xml.etree.ElementTree as ET
from xml.dom import minidom
from typing import Dict, List, Any
from dataclasses import dataclass
import xmltodict

from .decorators import newobj


@dataclass
class ToolConnection:
    tool_id: int = 0
    output: str = 'Output'
    input: str = 'Input'


@dataclass
class ToolPosition:
    x: int = 0
    y: int = 0


class Tool:
    """
    Base class for representing an Alteryx tool (or Node in the workflow XML).
    """

    def __init__(self, tool_id: int):
        self._tool_id: int = tool_id
        self._plugin: str = ''
        self._position: ToolPosition = ToolPosition()
        self._engine_dll: str = ''
        self._engine_dll_entry_point: str = ''
        self._inputs: List[ToolConnection] = list()
        self._outputs: List[ToolConnection] = list()
        self._properties: Dict[str, Any] = dict({})
        self._can_have_input: bool = True
        self._can_have_output: bool = True

    @property
    def tool_id(self) -> int:
        return self._tool_id

    @tool_id.setter
    def tool_id(self, value: int) -> None:
        self._tool_id = value

    @property
    def plugin(self) -> str:
        return self._plugin

    @plugin.setter
    def plugin(self, value: str) -> None:
        self._plugin = value

    @property
    def position(self) -> ToolPosition:
        return self._position

    @position.setter
    def position(self, value: ToolPosition) -> None:
        self._position = value

    @property
    def engine_dll(self) -> str:
        return self._engine_dll

    @engine_dll.setter
    def engine_dll(self, value: str) -> None:
        self._engine_dll = value

    @property
    def engine_dll_entry_point(self) -> str:
        return self._engine_dll_entry_point

    @engine_dll_entry_point.setter
    def engine_dll_entry_point(self, value: str) -> None:
        self._engine_dll_entry_point = value

    @property
    def inputs(self) -> List[ToolConnection]:
        return self._inputs

    @inputs.setter
    def inputs(self, value: List[ToolConnection]):
        self._inputs = value

    @property
    def outputs(self) -> List[ToolConnection]:
        return self._outputs

    @outputs.setter
    def outputs(self, value: List[ToolConnection]):
        self._outputs = value

    @property
    def properties(self) -> Dict[str, Any]:
        return self._properties

    @properties.setter
    def properties(self, value: Dict[str, Any]) -> None:
        self._properties = value

    def can_have_input(self) -> bool:
        return self._can_have_input

    def _can_have_input(self, value: bool) -> None:
        self._can_have_input = value

    def can_have_output(self) -> bool:
        return self._can_have_output

    def _can_have_output(self, value: bool) -> None:
        self._can_have_output = value

    def is_source(self) -> bool:
        return len(self._inputs) == 0

    def is_sink(self) -> bool:
        return len(self._outputs) == 0

    def is_orphan(self) -> bool:
        return self.is_source() and self.is_sink()

    @newobj
    def add_input(self, tool_id: str, output: str, input: str) -> '__class__':
        if self._can_have_input:
            self.inputs.append(ToolConnection(tool_id=tool_id, output=output, input=input))
        else:
            raise RuntimeWarning(f"Cannot add an input to a {type(self).__name__}")

    @newobj
    def add_output(self, tool_id: str, output: str, input: str) -> '__class__':
        if self._can_have_output:
            self.outputs.append(ToolConnection(tool_id=tool_id, output=output, input=input))
        else:
            raise RuntimeWarning(f"Cannot add an output to a {type(self).__name__}")

    def toxml(self) -> ET.Element:
        """Outputs an ElementTree.Element containing an XML representation of the tool
        """
        root: ET.Element = ET.Element('Root') # Dummy element that will be eliminated if used to extend other XML

        tool: ET.SubElement = ET.SubElement(root, 'Node')
        tool.set('ToolID', str(self.tool_id))

        gui_settings: ET.SubElement = ET.SubElement(tool, 'GuiSettings')
        gui_settings.set('Plugin', self.plugin)
        pos: ET.SubElement = ET.SubElement(gui_settings, 'Position')
        pos.set('x', str(self.position.x))
        pos.set('y', str(self.position.y))

        xml: str = xmltodict.unparse({'Root':{'Properties':self.properties}})
        properties: ET.Element = ET.fromstring(xml)
        tool.extend(properties)

        engine_settings: ET.SubElement = ET.SubElement(tool, 'EngineSettings')
        engine_settings.set('EngineDll', self.engine_dll)
        engine_settings.set('EngineDllEntryPoint', self.engine_dll_entry_point)

        return root

    def __repr__(self) -> str:
        xml = self.toxml()
        text = ET.tostring(xml, 'utf-8')
        parsed = minidom.parseString(text)
        return parsed.toprettyxml(indent='  ').replace('&quot;', '"')
