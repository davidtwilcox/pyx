from ayxproperty import AyxProperty
from tool import Tool
from field import Field
from xml.dom import minidom
import xml.etree.ElementTree as ET
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class SelectField:
    """
    Contains information for a field that may or may not be selected in the tool
    """
    field: str = ''
    selected: bool = False

@dataclass
class SelectToolConfiguration:
    """
    Contains configuration information for an SelectTool instance.
    """
    order_changed: bool = False
    comma_decimal: bool = False

class SelectTool(Tool):
    """
    Represents an Input tool in an Alteryx workflow.
    """
    def __init__(self, tool_id: str, configuration: SelectToolConfiguration, select_fields: List[SelectField]):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.AlteryxSelect.AlteryxSelect'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxSelect'
        self.inputs.append('Input')
        self.outputs.append('Output')

        self.configuration = configuration
        self.select_fields = select_fields

    def __set_configuration__(self) -> None:
        self.guisettings: Dict[str, AyxProperty] = dict({
            'Position': AyxProperty('Position').set_attribute('x', str(self.position[0])).set_attribute('y', str(self.position[1]))
        })

        fields: List[AyxProperty] = list()
        for field in self.select_fields:
            fields.append(
                AyxProperty('SelectField')
                .set_attribute('field', field.field)
                .set_attribute('selected', str(field.selected))
            )

        self.properties: Dict[str, AyxProperty] = dict({
            'Configuration': AyxProperty('Configuration').add_child(
                AyxProperty('OrderChanged', str(self.configuration.order_changed))
            ).add_child(
                AyxProperty('CommaDecimal', str(self.configuration.comma_decimal))
            ).add_child(
                AyxProperty('SelectFields').add_children(fields)
            ),
            'Annotation': AyxProperty('Annotation')
                .set_attribute('DisplayMode', '0')
                .add_child(AyxProperty('Name'))
                .add_child(AyxProperty('DefaultAnnotationText'))
                .add_child(AyxProperty('Left').set_attribute('value', 'False'))
        })

        self.engine_settings = AyxProperty('EngineSettings').set_attribute('EngineDll', self.engine_dll).set_attribute('EngineDllEntryPoint', self.engine_dll_entry_point)

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the tool.
        """
        self.__set_configuration__()
        
        # Dummy element that ElementTree extend() will strip
        root = ET.Element('root')

        node = ET.SubElement(root, 'Node')
        node.set('ToolID', self.tool_id)

        guisettings = ET.SubElement(node, 'GuiSettings')
        guisettings.set('Plugin', self.plugin)
        for _, guisettings_val in self.guisettings.items():
            xml = guisettings_val.toxml()
            guisettings.extend(xml)

        properties = ET.SubElement(node, 'Properties')
        for _, prop_val in self.properties.items():
            xml = prop_val.toxml()
            properties.extend(xml)        

        node.extend(self.engine_settings.toxml())

        return root

