from pyx.workflow import Workflow
from pyx.workflow import ToolPosition
from pyx.outputtool import OutputTool

def main():
    workflow: Workflow = Workflow.read('workflows/Example-Simple2.yxmd')

    outputTool: OutputTool = OutputTool(7)
    outputTool.position = ToolPosition(x=workflow.tools[6].position.x, y=workflow.tools[6].position.y + 100)
    workflow.add_tool(outputTool)
    workflow.add_connection(5, 'Output', 7, 'Input')

    workflow.filename = 'workflows/Example-1-Output.yxmd'
    Workflow.write(workflow)

if __name__ == '__main__':
    main()