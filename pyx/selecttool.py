from .tool import Tool
from typing import Dict, Any

from .decorators import newobj


class SelectTool(Tool):
    """
    Represents a Select tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: str):
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

