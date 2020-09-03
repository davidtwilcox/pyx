from .tool import Tool
from typing import Dict, Any

from .decorators import newobj


class SortTool(Tool):
    """
    Represents a Sort tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: str):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.Sort.Sort'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxSort'