from workflow import Workflow
from inputtool import InputToolConfiguration, InputTool

def main():
    input_tool_cfg = InputToolConfiguration(
        InputFileName='C:\\Data\\records.csv',
        HeaderRow=True
    )
    input_tool = InputTool('1', input_tool_cfg)

    workflow = Workflow('Simple', '2019.3')
    workflow.add_tool(input_tool)
    workflow.write()

if __name__ == '__main__':
    main()