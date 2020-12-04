# Pyx, a Python module for creating, reading, and editing Alteryx Designer workflows entirely in code
# Copyright (C) 2020  David T. Wilcox

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

    def __init__(self, tool_id: int):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.DbFileOutput.DbFileOutput'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxDbFileOutput'

        super()._can_have_output(False)