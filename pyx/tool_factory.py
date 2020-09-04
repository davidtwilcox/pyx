from typing import Dict

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
    registry: Dict[str, type] = {
        'AlteryxBasePluginsGui.DbFileInput.DbFileInput': InputTool,
        'AlteryxBasePluginsGui.AlteryxSelect.AlteryxSelect': SelectTool,
        'AlteryxBasePluginsGui.AutoField.AutoField': AutofieldTool,
        'AlteryxBasePluginsGui.Filter.Filter': FilterTool,
        'AlteryxBasePluginsGui.Sort.Sort': SortTool,
        'AlteryxBasePluginsGui.DbFileOutput.DbFileOutput': OutputTool,
    }

    @staticmethod
    def create_tool(plugin: str, tool_id: str) -> Tool:
        if plugin in ToolFactory.registry:
            return ToolFactory.registry[plugin](tool_id)
        else:
            return Tool(tool_id)