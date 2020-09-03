from typing import Dict, Any

from .tool import Tool


class InputTool(Tool):
    """
    Represents an Input tool in an Alteryx workflow.
    """

    def __init__(self, tool_id: str):
        super().__init__(tool_id)
        self.plugin = 'AlteryxBasePluginsGui.DbFileInput.DbFileInput'
        self.engine_dll = 'AlteryxBasePluginsEngine.dll'
        self.engine_dll_entry_point = 'AlteryxDbFileInput'

        super()._can_have_input(False)

    @property
    def input_file_name(self) -> str:
        return self._file_config['#text']

    @input_file_name.setter
    def input_file_name(self, value: str) -> None:
        self._file_config['#text'] = value

    @property
    def record_limit(self) -> int:
        return int(self._file_config['@RecordLimit'])

    @record_limit.setter
    def record_limit(self, value: int) -> None:
        self._file_config['@RecordLimit'] = str(value)

    @property
    def search_sub_dirs(self) -> bool:
        return bool(self._file_config['SearchSubDirs'])

    @search_sub_dirs.setter
    def search_sub_dirs(self, value: bool) -> None:
        self._file_config['SearchSubDirs'] = str(value)

    @property
    def file_format(self) -> int:
        return int(self._file_config['FileFormat'])

    @file_format.setter
    def file_format(self, value: int) -> None:
        self._file_config['FileFormat'] = str(value)

    @property
    def code_page(self) -> int:
        return int(self._format_specific_options['CodePage']['#text'])

    @code_page.setter
    def code_page(self, value: int) -> None:
        self._format_specific_options['CodePage']['#text'] = str(value)

    @property
    def delimiter(self) -> str:
        return self._format_specific_options['Delimeter']['#text']

    @delimiter.setter
    def delimiter(self, value: str) -> None:
        self._format_specific_options['Delimeter']['#text'] = value

    @property
    def ignore_errors(self) -> bool:
        return bool(self._format_specific_options['IgnoreErrors']['#text'])

    @ignore_errors.setter
    def ignore_errors(self, value: bool) -> None:
        self._format_specific_options['IgnoreErrors']['#text'] = str(value)

    @property
    def field_length(self) -> int:
        return int(self._format_specific_options['FieldLen']['#text'])

    @field_length.setter
    def field_length(self, value: int) -> None:
        self._format_specific_options['FieldLen']['#text'] = str(value)

    @property
    def allow_shared_write(self) -> bool:
        return bool(self._format_specific_options['AllowShareWrite']['#text'])

    @allow_shared_write.setter
    def allow_shared_write(self, value: bool) -> None:
        self._format_specific_options['AllowShareWrite']['#text'] = str(value)

    @property
    def header_row(self) -> bool:
        return bool(self._format_specific_options['HeaderRow']['#text'])

    @header_row.setter
    def header_row(self, value: bool) -> None:
        self._format_specific_options['HeaderRow']['#text'] = str(value)

    @property
    def ignore_quotes(self) -> str:
        return self._format_specific_options['IgnoreQuotes']['#text']

    @ignore_quotes.setter
    def ignore_quotes(self, value: str) -> None:
        self._format_specific_options['IgnoreQuotes']['#text'] = value

    @property
    def import_line(self) -> int:
        return int(self._format_specific_options['ImportLine']['#text'])

    @import_line.setter
    def import_line(self, value: int) -> None:
        self._format_specific_options['ImportLine']['#text'] = str(value)

    @property
    def _file_config(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['File']
        else:
            raise NameError('Properties does not contain Configuration > File')

    @property
    def _format_specific_options(self) -> Dict[str, Any]:
        if self.properties:
            return self.properties['Configuration']['FormatSpecificOptions']
        else:
            raise NameError('Properties does not contain Configuration > FormatSpecificOptions')
