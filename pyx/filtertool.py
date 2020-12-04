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
from enum import Enum
from datetime import datetime


class FilterMode(Enum):
    SIMPLE = 'Simple'
    CUSTOM = 'Custom'

    def __str__(self) -> str:
        return self.value


class FilterOperator(Enum):
    IS_FALSE = 'IsFalse'
    IS_TRUE = 'IsTrue'
    IS_EMPTY = 'IsEmpty'
    IS_NOT_EMPTY = 'IsNotEmpty'
    IS_NULL = 'IsNull'
    IS_NOT_NULL = 'IsNotNull'
    EQUAL = '='
    NOT_EQUAL = '!='
    GREATER_THAN = '&gt;'
    GREATER_THAN_OR_EQUAL = '&gt;='
    LESS_THAN = '&lt;'
    LESS_THAN_OR_EQUAL = '&lt;='
    CONTAINS = 'Contains'
    DOES_NOT_CONTAIN = 'NotContains'
    DATE_RANGE = 'DateRange'
    PERIOD_AFTER = 'PeriodAfter'
    PERIOD_BEFORE = 'PeriodBefore'

    def __str__(self) -> str:
        return self.value


class FilterDateType(Enum):
    FIXED = 'Fixed'
    YESTERDAY = 'Yesterday'
    TODAY = 'Today'
    TOMORROW = 'Tomorrow'

    def __str__(self) -> str:
        return self.value


class FilterPeriodType(Enum):
    DAYS = 'Days'
    WEEKS = 'Weeks'
    MONTHS = 'Months'
    QUARTERS = 'Quarters'
    YEARS = 'Years'

    def __str__(self) -> str:
        return self.value


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
    def filter_mode(self) -> FilterMode:
        return FilterMode(self._configuration['Mode']['#text'])

    @filter_mode.setter
    def filter_mode(self, value: FilterMode) -> None:
        self._configuration['Mode']['#text'] = str(value)

    @property
    def operator(self) -> FilterOperator:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter operator when not in simple mode')
        else:
            return FilterOperator(self._config_simple['Operator']['#text'])

    @operator.setter
    def operator(self, value: FilterOperator) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter operator when not in simple mode')
        else:
            self._config_simple['Operator']['#text'] = str(value)

    @property
    def field(self) -> str:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter field when not in simple mode')
        else:
            return self._config_simple['Field']['#text']

    @field.setter
    def field(self, value: str) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter field when not in simple mode')
        else:
            if value == '':
                raise ValueError('Filter field cannot be empty.')
            self._config_simple['Field']['#text'] = value

    @property
    def operand(self) -> str:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter operand when not in simple mode')
        else:
            return self._config_simple['Operands']['Operand']['#text']

    @operand.setter
    def operand(self, value: str) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter operand when not in simple mode')
        else:
            self._config_simple['Operands']['Operand']['#text'] = value

    @property
    def ignore_time_in_datetime(self) -> bool:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter ignore time in datetime flag when not in simple mode')
        else:
            return bool(self._config_simple['Operands']['IgnoreTimeInDateTime']['#text'])

    @ignore_time_in_datetime.setter
    def ignore_time_in_datetime(self, value: bool) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter ignore time in datetime flag  when not in simple mode')
        else:
            self._config_simple['Operands']['IgnoreTimeInDateTime']['#text'] = str(value)

    @property
    def date_type(self) -> FilterDateType:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter date type when not in simple mode')
        else:
            return FilterDateType(self._config_simple['Operands']['DateType']['#text'])

    @date_type.setter
    def date_type(self, value: FilterDateType) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter date type when not in simple mode')
        else:
            self._config_simple['Operands']['DateType']['#text'] = str(value)

    @property
    def period_date(self) -> datetime:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter period date when not in simple mode')
        else:
            return datetime.strptime(self._config_simple['Operands']['PeriodDate']['#text'],
                                     '%Y-%m-%d %H:%M:%S')

    @period_date.setter
    def period_date(self, value: datetime) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter period date when not in simple mode')
        else:
            self._config_simple['Operands']['PeriodDate']['#text'] = value.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def period_type(self) -> FilterPeriodType:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter period type when not in simple mode')
        else:
            return FilterPeriodType(self._config_simple['Operands']['PeriodType']['#text'])

    @period_type.setter
    def period_type(self, value: FilterPeriodType) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter period type when not in simple mode')
        else:
            self._config_simple['Operands']['PeriodType']['#text'] = str(value)

    @property
    def period_count(self) -> int:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter period count when not in simple mode')
        else:
            return int(self._config_simple['Operands']['PeriodCount']['#text'])

    @period_count.setter
    def period_count(self, value: int) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter period count when not in simple mode')
        else:
            self._config_simple['Operands']['PeriodCount']['#text'] = str(value)

    @property
    def start_date(self) -> datetime:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter start date when not in simple mode')
        else:
            return datetime.strptime(self._config_simple['Operands']['StartDate']['#text'],
                                     '%Y-%m-%d %H:%M:%S')

    @start_date.setter
    def start_date(self, value: datetime) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter start date when not in simple mode')
        else:
            self._config_simple['Operands']['StartDate']['#text'] = value.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def end_date(self) -> datetime:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot get filter start date when not in simple mode')
        else:
            return datetime.strptime(self._config_simple['Operands']['EndDate']['#text'],
                                     '%Y-%m-%d %H:%M:%S')

    @end_date.setter
    def end_date(self, value: datetime) -> None:
        if self.filter_mode != FilterMode.SIMPLE:
            raise RuntimeWarning('Cannot set filter end date when not in simple mode')
        else:
            self._config_simple['Operands']['EndDate']['#text'] = value.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def expression(self) -> str:
        if self.filter_mode != FilterMode.CUSTOM:
            raise RuntimeWarning('Cannot get filter expression when not in custom mode')
        else:
            return self._configuration['Expression']['#text']

    @expression.setter
    def expression(self, value: str) -> None:
        if self.filter_mode != FilterMode.CUSTOM:
            raise RuntimeWarning('Cannot set filter expression when not in custom mode')
        else:
            if value == '':
                raise ValueError('Filter expression cannot be empty.')
            self._configuration['Expression']['#text'] = value

    @property
    def _configuration(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']
        else:
            raise NameError('Properties does not contain Configuration')

    @property
    def _config_simple(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['Simple']
        else:
            raise NameError('Properties does not contain Configuration > Simple')

