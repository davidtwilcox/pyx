from .tool import Tool
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class OutputToolConfiguration:
    """
    Contains configuration information for an OutputTool isntance.
    """
    output_file_name: str = ''
    max_records: int = -1 
    file_format: int = 0
    line_end_style: str = 'CRLF'
    delimiter: str = ','
    force_quotes: bool = False
    header_row: bool = True
    code_page: int = 28591
    write_bom: bool = True
    multi_file: bool = False


class OutputTool(Tool):
    """
    Represents an Output tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: str, configuration: OutputToolConfiguration):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.DbFileOutput.DbFileOutput'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxDbFileOutput'

        super()._can_have_output = False