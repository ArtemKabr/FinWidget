from pathlib import Path

import pandas as pd
import pytest

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
