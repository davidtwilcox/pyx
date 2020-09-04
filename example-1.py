from pyx.workflow import Workflow
from pyx.outputtool import OutputTool

def main():
    workflow: Workflow = Workflow.read('workflows/Example-Simple2.yxmd')

    outputTool: OutputTool = OutputTool(workflow.get_new_tool_id())
    outputTool.position = workflow.position_below(6)

    workflow.add_tool(outputTool) \
            .add_connection(5, 'Output', outputTool.tool_id, 'Input')

    workflow.tools[3].set_field('Responder', False)

    Workflow.write(workflow, 'workflows/Example-1-Output.yxmd')

if __name__ == '__main__':
    main()