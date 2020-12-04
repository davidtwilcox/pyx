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
from typing import Dict, Any

from .decorators import newobj


class SelectTool(Tool):
    """
    Represents a Select tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: int):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.AlteryxSelect.AlteryxSelect'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxSelect'

    @property
    def order_changed(self) -> bool:
        return bool(self._configuration['OrderChanged']['@value'])

    @order_changed.setter
    def order_changed(self, value: bool) -> None:
        self._configuration['OrderChanged']['@value'] = str(value)

    @property
    def comma_decimal(self) -> bool:
        return bool(self._configuration['CommaDecimal']['@value'])

    @comma_decimal.setter
    def comma_decimal(self, value: bool) -> None:
        self._configuration['CommaDecimal']['@value'] = str(value)

    @newobj
    def set_select_field(self, field: str, selected: bool) -> '__class__':
        pass

    @newobj
    def remove_select_field(self, field: str) -> '__class__':
        pass

    @property
    def _configuration(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']
        else:
            raise NameError('Properties does not contain Configuration')

    @property
    def _select_fields(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['SelectFields']
        else:
            raise NameError('Properties does not contain Configuration > SelectFields')

