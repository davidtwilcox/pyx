from .tool import Tool
from typing import Dict, Any

from .decorators import newobj


class AutofieldTool(Tool):
    """
    Represents an Autofield tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: str):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.AutoField.AutoField'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxAutoField'

    @newobj
    def set_field(self, field: str, selected: bool) -> '__class__':
        pass

    @newobj
    def remove_field(self, field: str) -> '__class__':
        pass

    @property
    def _fields(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['Fields']
        else:
            raise NameError('Properties does not contain Configuration > Fields')