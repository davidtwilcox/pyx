from .tool import Tool
from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class FilterMode(Enum):
    SIMPLE = 1
    CUSTOM = 2


@dataclass
class FilterToolConfiguration:
    """
    Contains configuration information for a FilterTool instance.
    """
    expression: str = ''
    filter_mode: FilterMode = FilterMode.SIMPLE
    field: str = ''
    operand: str = ''
    operator: str = ''
    ignore_time_in_datetime: bool = True
    date_type: str = 'fixed'
    period_date: str = ''
    period_type: str = ''
    period_count: int = 0
    start_date: str = ''
    end_date: str = ''


class FilterTool(Tool):
    """
    Represents a Filter tool in an Alteryx workflow.
    """
    def __init__(self, tool_id: int):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.Filter.Filter'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxFilter'

    @property
    def _configuration(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']
        else:
            raise NameError('Properties does not contain Configuration')

