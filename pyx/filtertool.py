from ayxproperty import AyxProperty
from tool import Tool
from field import Field
from xml.dom import minidom
import xml.etree.ElementTree as ET
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class FilterMode(Enum):
    SIMPLE = 1
    CUSTOM = 2

@dataclass
class FilterToolConfiguration:
    """
    Contains configuration information for a FilterTool instance.
    """
    expression: str = ''
    filter_mode: FilterMode = FilterMode.SIMPLE
    field: str = ''
    operand: str = ''
    operator: str = ''
    ignore_time_in_datetime: bool = True
    date_type: str = 'fixed'
    period_date: str = ''
    period_type: str = ''
    period_count: int = 0
    start_date: str = ''
    end_date: str = ''

class FilterTool(Tool):
    """
    Represents a Filter tool in an Alteryx workflow.
    """
    def __init__(self, tool_id: str, configuration: FilterToolConfiguration):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.Filter.Filter'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxFilter'
        self.inputs.append('Input')
        self.outputs.append('True')
        self.outputs.append('False')

        self.configuration = configuration

    def __set_configuration__(self) -> None:
        self.guisettings: Dict[str, AyxProperty] = dict({
            'Position': AyxProperty('Position').set_attribute('x', str(self.position[0])).set_attribute('y', str(self.position[1]))
        })

        configuration: AyxProperty = None
        if self.configuration.filter_mode == FilterMode.SIMPLE:
            configuration = AyxProperty('Configuration').add_child(
                AyxProperty('Mode', 'Simple')
            ).add_child(
                AyxProperty('Simple')
                .add_child(AyxProperty('Operator', self.configuration.operator))
                .add_child(AyxProperty('Field', self.configuration.field))
                .add_child(AyxProperty('Operands')
                    .add_child(AyxProperty('IgnoreTimeInDateTime', str(self.configuration.ignore_time_in_datetime)))
                    .add_child(AyxProperty('DateType', self.configuration.date_type))
                    .add_child(AyxProperty('PeriodDate', self.configuration.period_date))
                    .add_child(AyxProperty('PeriodType'))
                    .add_child(AyxProperty('PeriodCount', str(self.configuration.period_count)))
                    .add_child(AyxProperty('Operand', self.configuration.operand))
                    .add_child(AyxProperty('StartDate', self.configuration.start_date))
                    .add_child(AyxProperty('EndDate', self.configuration.end_date))
                )
            )
        elif self.configuration.filter_mode == FilterMode.CUSTOM:
            configuration = AyxProperty('Configuration').add_child(
                AyxProperty('Mode', 'Custom')
            ).add_child(
                AyxProperty('Expression', self.configuration.expression)
            )

        self.properties: Dict[str, AyxProperty] = dict({
            'Configuration': configuration,
            'Annotation': AyxProperty('Annotation')
                .set_attribute('DisplayMode', '0')
                .add_child(AyxProperty('Name'))
                .add_child(AyxProperty('DefaultAnnotationText', self.configuration.expression))
                .add_child(AyxProperty('Left', 'False'))
        })

        self.engine_settings = AyxProperty('EngineSettings').set_attribute('EngineDll', self.engine_dll).set_attribute('EngineDllEntryPoint', self.engine_dll_entry_point)

    def toxml(self) -> ET.Element:
        """
        Returns an XML representation of the tool.
        """
        self.__set_configuration__()
        
        # Dummy element that ElementTree extend() will strip
        root: ET.Element = ET.Element('root')

        node: ET.SubElement = ET.SubElement(root, 'Node')
        node.set('ToolID', self.tool_id)

        guisettings: ET.SubElement = ET.SubElement(node, 'GuiSettings')
        guisettings.set('Plugin', self.plugin)
        for _, guisettings_val in self.guisettings.items():
            xml: ET.Element = guisettings_val.toxml()
            guisettings.extend(xml)

        properties = ET.SubElement(node, 'Properties')
        for _, prop_val in self.properties.items():
            xml: ET.Element = prop_val.toxml()
            properties.extend(xml)        

        node.extend(self.engine_settings.toxml())

        return root

