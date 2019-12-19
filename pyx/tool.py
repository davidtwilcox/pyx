from xml.dom import minidom
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Tuple, List

class Tool(ABC):
    """
    Base class for representing an Alteryx tool (or Node in the workflow XML).
    """

    def __init__(self, tool_id: str):
        self.tool_id: str = tool_id
        self.position: Tuple[int, int] = (0, 0)
        self.plugin: str = ''
        self.engine_dll: str = ''
        self.engine_dll_entry_point: str = ''
        self.inputs: List[str] = list()
        self.outputs: List[str] = list()
        super().__init__()

    def num_inputs(self) -> int:
        return len(self.inputs)

    def num_outputs(self) -> int:
        return len(self.outputs)

    def _optional_numeric_value(self, value: int) -> str:
        if value < 0:
            return ''
        else:
            return str(value)

    @abstractmethod
    def toxml(self) -> ET.Element:
        pass
