from unittest.mock import MagicMock, patch

from src.copy_operations_file import copy_operations_file


@patch("builtins.print")
@patch("src.copy_operations_file.shutil.copy")
@patch("src.copy_operations_file.Path.mkdir")
def test_copy_success(mock_mkdir: MagicMock, mock_copy: MagicMock, mock_print: MagicMock) -> None:
    copy_operations_file()
    mock_copy.assert_called_once()
    mock_mkdir.assert_called_once()
    mock_print.assert_called_with("✅ Файл скопирован в: data/operations3.xlsx")


@patch("builtins.print")
@patch("src.copy_operations_file.shutil.copy", side_effect=FileNotFoundError)
@patch("src.copy_operations_file.Path.mkdir")
def test_copy_file_not_found(mock_mkdir: MagicMock, mock_copy: MagicMock, mock_print: MagicMock) -> None:
    copy_operations_file()
    mock_print.assert_called_with("❌ Файл не найден: C:/Users/HP/Desktop/operations3.xlsx")
