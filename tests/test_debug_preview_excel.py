from unittest.mock import MagicMock, patch

import pandas as pd

from src import debug_preview_excel


@patch("builtins.print")
@patch("src.debug_preview_excel.pd.read_excel")
def test_preview_success(mock_read_excel: MagicMock, mock_print: MagicMock) -> None:
    df = pd.DataFrame([{"a": "1", "b": "2"}, {"a": "3", "b": "4"}])
    mock_read_excel.return_value = df

    debug_preview_excel.main()

    mock_print.assert_any_call("Первые 2 строки Excel-файла:")
    mock_print.assert_any_call({"a": "1", "b": "2"})
    mock_print.assert_any_call({"a": "3", "b": "4"})


@patch("builtins.print")
@patch("src.debug_preview_excel.pd.read_excel", side_effect=Exception("ошибка"))
def test_preview_fail(mock_read_excel: MagicMock, mock_print: MagicMock) -> None:
    debug_preview_excel.main()

    mock_print.assert_called_with("Ошибка при чтении Excel-файла: ошибка")
