from .ayxproperty import AyxProperty
from .tool import Tool
from .field import Field
import xml.etree.ElementTree as ET
from typing import Dict, List
from dataclasses import dataclass
import os


@dataclass
class InputToolConfiguration:
    """
    Contains configuration information for an InputTool instance.
    """
    input_file_name: str = ''
    record_limit: str = ''
    search_sub_dirs: bool = False
    file_format: int = 0
    code_page: int = 28591
    delimiter: str = ','
    ignore_errors: bool = False
    field_length: int = 254
    allow_shared_write: bool = False
    header_row: bool = False
    ignore_quotes: str = 'DoubleQuotes'
    import_line: int = 1


class InputTool(Tool):
    """
    Represents an Input tool in an Alteryx workflow.
    """
    def __init__(self, tool_id: str, configuration: InputToolConfiguration, record_info: List[Field]):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.DbFileInput.DbFileInput'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxDbFileInput'
        self.outputs.append('Output')

        self.configuration = configuration
        self.record_info = record_info

    def __set_configuration__(self) -> None:
        self.guisettings: Dict[str, AyxProperty] = dict({
            'Position': AyxProperty('Position').set_attribute('x', str(self.position[0])).set_attribute('y', str(self.position[1]))
        })

        fields: List[AyxProperty] = list()
        for field in self.record_info:
            fields.append(
                AyxProperty('Field')
                .set_attribute('name', field.name)
                .set_attribute('size', str(field.size))
                .set_attribute('source', 'File: ' + self.configuration.input_file_name)
                .set_attribute('type', str(field.alteryx_type.name))
            )

        self.properties: Dict[str, AyxProperty] = dict({
            'Configuration': AyxProperty('Configuration').add_child(
                AyxProperty('Passwords')
            ).add_child(
                AyxProperty('File', self.configuration.input_file_name)
                .set_attribute('OutputFileName', '')
                .set_attribute('RecordLimit', str(self.configuration.record_limit))
                .set_attribute('SearchSubDirs', str(self.configuration.search_sub_dirs))
                .set_attribute('FileFormat', str(self.configuration.file_format))
            ).add_child(
                AyxProperty('FormatSpecificOptions')
                .add_child(AyxProperty('CodePage', str(self.configuration.code_page)))
                .add_child(AyxProperty('Delimeter', self.configuration.delimiter))
                .add_child(AyxProperty('IgnoreErrors', str(self.configuration.ignore_errors)))
                .add_child(AyxProperty('FieldLen', str(self.configuration.field_length)))
                .add_child(AyxProperty('AllowSharedWrite', str(self.configuration.allow_shared_write)))
                .add_child(AyxProperty('HeaderRow', str(self.configuration.header_row)))
                .add_child(AyxProperty('IgnoreQuotes', self.configuration.ignore_quotes))
                .add_child(AyxProperty('ImportLine', str(self.configuration.import_line)))
            ),
            'Annotation': AyxProperty('Annotation')
                .set_attribute('DisplayMode', '0')
                .add_child(AyxProperty('Name'))
                .add_child(AyxProperty('DefaultAnnotationText', os.path.basename(self.configuration.input_file_name)))
                .add_child(AyxProperty('Left').set_attribute('value', 'False')),
            'Dependencies': AyxProperty('Dependencies')
                .add_child(AyxProperty('Implicit')),
            'MetaInfo': AyxProperty('MetaInfo')
                .set_attribute('connection', 'Output')
                .add_child(AyxProperty('RecordInfo').add_children(fields))
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

