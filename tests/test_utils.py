from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src import utils
from src.utils import load_transactions_from_excel


def test_load_transactions_from_excel(tmp_path: Path) -> None:
    df = pd.DataFrame(
        [
            {"id": 1, "amount": 100, "operation_date": datetime(2024, 4, 15, 10, 0)},
            {"id": 2, "amount": 200, "operation_date": datetime(2024, 4, 16, 14, 30)},
        ]
    )
    file_path = tmp_path / "test.xlsx"

    # Сохраняем файл
    df.to_excel(file_path, index=False, engine="openpyxl")

    # Читаем и переименовываем
    read_df = pd.read_excel(file_path)
    read_df = read_df.rename(columns={"operation_date": "Дата операция"})
    read_df["Дата операция"] = pd.to_datetime(read_df["Дата операция"], dayfirst=True)

    result = read_df.to_dict(orient="records")

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["amount"] == 200
    assert isinstance(result[0]["Дата операция"], datetime)


def test_load_transactions_file_not_found() -> None:
    with pytest.raises(RuntimeError):
        load_transactions_from_excel("non_existing_file.xlsx")


@patch("requests.get")
def test_get_currency_rates(mock_get: Mock) -> None:
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"USD": 90, "EUR": 100}}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = utils.get_currency_rates(["USD", "EUR"])
    assert result == {"USD": 90.0, "EUR": 95.5}


@patch("requests.get")
def test_get_stock_prices(mock_get: Mock) -> None:
    def mock_json() -> dict[str, int]:
        return {"c": 150}

    mock_response = Mock()
    mock_response.json.side_effect = mock_json
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    result = utils.get_stock_prices(["AAPL", "AMZN", "GOOGL"])
    assert result == {"AAPL": 100.0, "AMZN": 150.0, "GOOGL": 200.0}
