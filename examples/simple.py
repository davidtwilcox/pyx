from workflow import Workflow
from field import Field
from inputtool import InputToolConfiguration, InputTool
from selecttool import SelectField, SelectToolConfiguration, SelectTool
from typing import List

def main():
    input_file_name: str = 'C:\\Program Files\\Alteryx\\Samples\\en\\SampleData\\Customers.csv'

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

    # Configure and create select tool
    select_tool_cfg: SelectToolConfiguration = SelectToolConfiguration()
    select_fields: List[SelectField] = [
        SelectField(field='Lat'),
        SelectField(field='Lon'),
        SelectField(field='Unknown', selected=True)
    ]
    select_tool: SelectTool = SelectTool('2', select_tool_cfg, select_fields)
    select_tool.position = (313, 66)

    # Configure, create, and write workflow
    workflow = Workflow('Simple', '2019.1')
    workflow \
        .add_tool(input_tool) \
        .add_tool(select_tool) \
        .add_connection(input_tool, 'Output', select_tool, 'Input') \
        .write()

if __name__ == '__main__':
    main()