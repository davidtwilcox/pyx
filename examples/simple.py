from pyx.workflow import Workflow
from pyx.field import Field
from pyx.inputtool import InputToolConfiguration, InputTool
from pyx.autofieldtool import AutofieldField, AutofieldTool
from pyx.filtertool import FilterMode,FilterToolConfiguration, FilterTool
from pyx.selecttool import SelectField, SelectToolConfiguration, SelectTool
from pyx.outputtool import OutputToolConfiguration, OutputTool
from typing import List


def main():
    input_file_name: str = 'C:\\Program Files\\Alteryx\\Samples\\en\\SampleData\\Customers.csv'
    output_file_name: str = 'C:\\Temp\\output.csv'

    # Configure and create input tool
    input_tool_cfg: InputToolConfiguration = InputToolConfiguration(
        input_file_name=input_file_name,
        header_row=True
    )
    source: str = 'File: ' + input_file_name
    record_info: List[Field] = [
        Field(name='Customer ID', source=source), 
        Field(name='Store Number', source=source),
        Field(name='Customer Segment', source=source),
        Field(name='Responder', source=source),
        Field(name='First Name', source=source),
        Field(name='Last Name', source=source),
        Field(name='Address', source=source),
        Field(name='City', source=source),
        Field(name='State', source=source),
        Field(name='Zip', source=source),
        Field(name='Lat', source=source),
        Field(name='Lon', source=source)
    ]
    input_tool: InputTool = InputTool('1', input_tool_cfg, record_info)
    input_tool.position = (78, 66)

    # Configure and create autofield tool
    autofield_fields: List[AutofieldField] = [
        AutofieldField(field='Customer ID'), 
        AutofieldField(field='Store Number'),
        AutofieldField(field='Customer Segment'),
        AutofieldField(field='Responder'),
        AutofieldField(field='First Name'),
        AutofieldField(field='Last Name'),
        AutofieldField(field='Address'),
        AutofieldField(field='City'),
        AutofieldField(field='State'),
        AutofieldField(field='Zip'),
        AutofieldField(field='Lat'),
        AutofieldField(field='Lon')
    ]
    autofield_tool: AutofieldTool = AutofieldTool('3', autofield_fields)
    autofield_tool.position = (196, 66)

    # Configure and create select tool
    select_tool_cfg: SelectToolConfiguration = SelectToolConfiguration()
    select_fields: List[SelectField] = [
        SelectField(field='Lat'),
        SelectField(field='Lon'),
        SelectField(field='*Unknown', selected=True)
    ]
    select_tool: SelectTool = SelectTool('2', select_tool_cfg, select_fields)
    select_tool.position = (313, 66)

    # Configure and create filter tool
    filter_tool_configuration: FilterToolConfiguration = FilterToolConfiguration(
        expression='[City] != "DENVER" AND [Responder] == "Yes"',
        filter_mode=FilterMode.CUSTOM
    )
    filter_tool: FilterTool = FilterTool('4', filter_tool_configuration)
    filter_tool.position = (407, 66)

    # Configure and create output tool
    output_tool_cfg: OutputToolConfiguration = OutputToolConfiguration(
        output_file_name=output_file_name
    )
    output_tool: OutputTool = OutputTool('6', output_tool_cfg)
    output_tool.position = (510, 54)

    # Configure, create, and write workflow
    workflow = Workflow('Simple', '2019.1')
    workflow \
        .add_tool(input_tool) \
        .add_tool(autofield_tool) \
        .add_tool(select_tool) \
        .add_tool(filter_tool) \
        .add_tool(output_tool) \
        .add_connection(input_tool, 'Output', autofield_tool, 'Input') \
        .add_connection(autofield_tool, 'Output', select_tool, 'Input') \
        .add_connection(select_tool, 'Output', filter_tool, 'Input') \
        .add_connection(filter_tool, 'True', output_tool, 'Input') \
        .write() \
        .run('"C:\\Program Files\\Alteryx\\bin\\AlteryxEngineCmd.exe"')


if __name__ == '__main__':
    main()