from .tool import Tool
from .inputtool import InputTool
from .selecttool import SelectTool
from .autofieldtool import AutofieldTool
from .filtertool import FilterTool
from .sorttool import SortTool
from .outputtool import OutputTool


class ToolFactory:
    """
    Creates a concrete tool class based on a plugin file name.
    """

    @staticmethod
    def create_tool(plugin: str, tool_id: str) -> Tool:
        if plugin == 'AlteryxBasePluginsGui.DbFileInput.DbFileInput':
            return InputTool(tool_id)
        elif plugin == 'AlteryxBasePluginsGui.AlteryxSelect.AlteryxSelect':
            return SelectTool(tool_id)
        elif plugin == 'AlteryxBasePluginsGui.AutoField.AutoField':
            return AutofieldTool(tool_id)
        elif plugin == 'AlteryxBasePluginsGui.Filter.Filter':
            return FilterTool(tool_id)
        elif plugin == 'AlteryxBasePluginsGui.Sort.Sort':
            return SortTool(tool_id)
        elif plugin == 'AlteryxBasePluginsGui.DbFileOutput.DbFileOutput':
            return OutputTool(tool_id)
        else:
            return Tool(tool_id)