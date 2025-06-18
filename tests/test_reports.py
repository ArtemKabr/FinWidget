import os

from src.reports import generate_filtered_report


def test_generate_filtered_report_creates_file() -> None:
    path = generate_filtered_report(status="OK", currency="RUB")
    assert os.path.exists(path)
    assert path.endswith(".xlsx")
