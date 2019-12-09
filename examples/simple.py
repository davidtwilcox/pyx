from workflow import Workflow
from field import Field
from inputtool import InputToolConfiguration, InputTool
from typing import List

def main():
    input_tool_cfg = InputToolConfiguration(
        InputFileName='C:\\Data\\records.csv',
        HeaderRow=True
    )

    record_info: List[Field] = [Field(Name='Customer ID'), Field(Name='Store Number')]

    input_tool = InputTool('1', input_tool_cfg, record_info)

    workflow = Workflow('Simple', '2019.1')
    workflow.add_tool(input_tool)
    workflow.write()

if __name__ == '__main__':
    main()