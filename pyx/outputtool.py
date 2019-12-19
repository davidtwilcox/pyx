from ayxproperty import AyxProperty
from tool import Tool
from field import Field
from xml.dom import minidom
import xml.etree.ElementTree as ET
from typing import Dict, List
from dataclasses import dataclass
import os

@dataclass
class OutputToolConfiguration:
    """
    Contains configuration information for an OutputTool isntance.
    """
    output_file_name: str = ''
    max_records: int = -1 
    file_format: int = 0
    line_end_style: str = 'CRLF'
    delimiter: str = ','
    force_quotes: bool = False
    header_row: bool = True
    code_page: int = 28591
    write_bom: bool = True
    multi_file: bool = False

class OutputTool(Tool):
    """
    Represents an Output tool in an Alteryx workflow.
    """
    def __init__(self, tool_id: str, configuration: OutputToolConfiguration):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.DbFileOutput.DbFileOutput'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxDbFileOutput'
        self.inputs.append('Input')
        
        self.configuration = configuration
        
    def __set_configuration__(self) -> None:
        self.guisettings: Dict[str, AyxProperty] = dict({
            'Position': AyxProperty('Position').set_attribute('x', str(self.position[0])).set_attribute('y', str(self.position[1]))
        })

        self.properties: Dict[str, AyxProperty] = dict({
            'Configuration': AyxProperty('Configuration').add_child(
                AyxProperty('Passwords')
            ).add_child(
                AyxProperty('File', self.configuration.output_file_name)
                .set_attribute('MaxRecords', self._optional_numeric_value(self.configuration.max_records))
                .set_attribute('FileFormat', str(self.configuration.file_format))
            ).add_child(
                AyxProperty('FormatSpecificOptions')
                .add_child(AyxProperty('LineEndStyle', self.configuration.line_end_style))
                .add_child(AyxProperty('Delimeter', self.configuration.delimiter))
                .add_child(AyxProperty('ForceQuotes', str(self.configuration.force_quotes)))
                .add_child(AyxProperty('HeaderRow', str(self.configuration.header_row)))
                .add_child(AyxProperty('CodePage', str(self.configuration.code_page)))
                .add_child(AyxProperty('WriteBOM', str(self.configuration.write_bom)))
            ).add_child(
                AyxProperty('MultiFile', str(self.configuration.multi_file))
            ),
            'Annotation': AyxProperty('Annotation')
                .set_attribute('DisplayMode', '0')
                .add_child(AyxProperty('Name'))
                .add_child(AyxProperty('DefaultAnnotationText', os.path.basename(self.configuration.output_file_name)))
                .add_child(AyxProperty('Left').set_attribute('value', 'False')),
            'Dependencies': AyxProperty('Dependencies')
                .add_child(AyxProperty('Implicit'))
        })

        self.engine_settings = AyxProperty('EngineSettings').set_attribute('EngineDll', self.engine_dll).set_attribute('EngineDllEntryPoint', self.engine_dll_entry_point)

    def toxml(self) -> ET.Element:
        """
        Returns an XML representation of the tool.
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