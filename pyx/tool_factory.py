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