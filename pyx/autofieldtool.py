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
from collections import OrderedDict
from typing import List, Dict, Tuple, Any

from .decorators import newobj


class AutofieldTool(Tool):
    """
    Represents an Autofield tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: int):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.AutoField.AutoField'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxAutoField'

    @newobj
    def set_field(self, field: str, selected: bool) -> '__class__':
        """Sets the specified field to selected or not in the tool configuration.
        """
        target: List[Any] = [f for f in self._fields if '@field' in f and f['@field'] == field]

        if target:
            for field in target:
                field['@selected'] = str(selected)
        else:
            self._fields.append(OrderedDict([('@field', field), ('@selected', str(selected))]))

    @newobj
    def get_field_selection(self, field: str) -> bool:
        """Returns the selection status of the specified field.

        Will return False if the field is not configured in the workflow.
        """
        target: List[Any] = [f for f in self._fields if '@field' in f and f['@field'] == field]

        if target:
            return '@selected' in target[0] and bool(target[0]['@selected'])
        else:
            return False

    @newobj
    def remove_field(self, field: str) -> '__class__':
        """Removes the specified field from the tool configuration.
        """
        self.properties['Configuration']['Fields']['Field'] = \
            [f for f in self._fields if '@field' in f and f['@field'] != field]

    def get_all_fields(self) -> List[Tuple[str, bool]]:
        """Returns a list of all fields configured in the tool.
        """
        all: List[Tuple[str, bool]] = \
            [(f['@field'], bool(f['@selected'])) for f in self._fields if '@field' in f and '@selected' in f]

        return all

    @property
    def _fields(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['Fields']['Field']
        else:
            raise NameError('Properties does not contain Configuration > Fields > Field')