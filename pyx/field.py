from xml.dom import minidom
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from enum import Enum

class AlteryxDataType(Enum):
    STRING = 1
    WSTRING = 2
    V_STRING = 3
    V_WSTRING = 4
    BYTE = 5
    INT16 = 6
    INT32 = 7
    INT64 = 8
    FIXED_DECIMAL = 9
    FLOAT = 10
    DOUBLE = 11
    DATE = 12
    TIME = 13
    DATE_TIME = 14
    BOOL = 15
    SPATIAL_OBJ = 16

@dataclass
class Field:
    Name: str = ''
    Size: int = 254
    Source: str = ''
    Type: AlteryxDataType = AlteryxDataType.V_STRING