from .tool import Tool
from typing import List, Dict, Any

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
        target: List[Dict[str, Any]] = [f for f in self._fields if f['@field'] == field]

        for field in target:
            field['@selected'] = selected

    @newobj
    def remove_field(self, field: str) -> '__class__':
        """Removes the specified field from the tool configuration.
        """
        pass

    @property
    def _fields(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['Fields']['Field']
        else:
            raise NameError('Properties does not contain Configuration > Fields > Field')