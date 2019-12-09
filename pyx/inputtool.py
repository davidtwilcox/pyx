from ayxproperty import AyxProperty
from tool import Tool
from field import Field
from xml.dom import minidom
import xml.etree.ElementTree as ET
from typing import Dict, List
from dataclasses import dataclass
import os

@dataclass
class InputToolConfiguration:
    """
    Contains configuration information for an InputTool instance.
    """
    InputFileName: str = ''
    RecordLimit: str = ''
    SearchSubDirs: bool = False
    FileFormat: int = 0
    CodePage: int = 28591
    Delimiter: str = ','
    IgnoreErrors: bool = False
    FieldLength: int = 254
    AllowSharedWrite: bool = False
    HeaderRow: bool = False
    IgnoreQuotes: str = 'DoubleQuotes'
    ImportLine: int = 1

class InputTool(Tool):
    """
    Represents an Input tool in an Alteryx workflow.
    """
    def __init__(self, tool_id: str, configuration: InputToolConfiguration, record_info: List[Field]):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.DbFileInput.DbFileInput'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxDbFileInput'

        self.configuration = configuration

        self.guisettings: Dict[str, AyxProperty] = dict({
            'Position': AyxProperty('Position').set_attribute('x', str(self.pos_x)).set_attribute('y', str(self.pos_y))
        })

        fields = list()
        for field in record_info:
            fields.append(
                AyxProperty('Field')
                .set_attribute('name', field.Name)
                .set_attribute('size', str(field.Size))
                .set_attribute('source', 'File: ' + self.configuration.InputFileName)
                .set_attribute('type', str(field.Type.name))
            )

        self.properties: Dict[str, AyxProperty] = dict({
            'Configuration': AyxProperty('Configuration').add_child(
                AyxProperty('Passwords')
            ).add_child(
                AyxProperty('File', self.configuration.InputFileName)
                .set_attribute('OutputFileName', '')
                .set_attribute('RecordLimit', str(self.configuration.RecordLimit))
                .set_attribute('SearchSubDirs', str(self.configuration.SearchSubDirs))
                .set_attribute('FileFormat', str(self.configuration.FileFormat))
            ).add_child(
                AyxProperty('FormatSpecificOptions')
                .add_child(AyxProperty('CodePage', str(self.configuration.CodePage)))
                .add_child(AyxProperty('Delimeter', self.configuration.Delimiter))
                .add_child(AyxProperty('IgnoreErrors', str(self.configuration.IgnoreErrors)))
                .add_child(AyxProperty('FieldLen', str(self.configuration.FieldLength)))
                .add_child(AyxProperty('AllowSharedWrite', str(self.configuration.AllowSharedWrite)))
                .add_child(AyxProperty('HeaderRow', str(self.configuration.HeaderRow)))
                .add_child(AyxProperty('IgnoreQuotes', self.configuration.IgnoreQuotes))
                .add_child(AyxProperty('ImportLine', str(self.configuration.ImportLine)))
            ),
            'Annotation': AyxProperty('Annotation')
                .set_attribute('DisplayMode', '0')
                .add_child(AyxProperty('Name'))
                .add_child(AyxProperty('DefaultAnnotationText', os.path.basename(self.configuration.InputFileName)))
                .add_child(AyxProperty('Left').set_attribute('value', 'False')),
            'Dependencies': AyxProperty('Dependencies')
                .add_child(AyxProperty('Implicit')),
            'MetaInfo': AyxProperty('MetaInfo')
                .set_attribute('connection', 'Output')
                .add_child(AyxProperty('RecordInfo').add_children(fields))
        })

        self.engine_settings = AyxProperty('EngineSettings').set_attribute('EngineDll', self.engine_dll).set_attribute('EngineDllEntryPoint', self.engine_dll_entry_point)

    def toxml(self) -> ET.Element:
        """Returns an XML representation of the tool.
        """
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

