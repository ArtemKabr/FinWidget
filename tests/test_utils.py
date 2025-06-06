from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src import utils
from src.utils import load_transactions_from_excel


def test_load_transactions_from_excel(tmp_path: Path) -> None:
    # Создаём временный Excel-файл
    df = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
    file_path = tmp_path / "test.xlsx"
    df.to_excel(file_path, index=False)

    result = load_transactions_from_excel(str(file_path))
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["amount"] == 200


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
