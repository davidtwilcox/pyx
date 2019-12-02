from tool import Tool

class InputTool(Tool):
    """
    Represents an Input tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: str, configuration: str = '', input_filename: str = ''):
        self.input_filename = input_filename
        super().__init__(tool_id, configuration)