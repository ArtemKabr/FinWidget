from unittest.mock import Mock, patch

from src.services import convert_to_rub

# import pytest — закомментировано, так как не используется


def test_convert_rub_no_conversion() -> None:
    """
    ✅ Проверка: если валюта RUB, сумма возвращается без изменений.
    """
    transaction = {"operationAmount": {"amount": "1500.00", "currency": {"code": "RUB"}}}

    result = convert_to_rub(transaction)
    assert result == 1500.0


@patch("src.services.requests.get")  # подмена requests.get
@patch("src.services.os.getenv", return_value="fake-api-key")  # подмена ключа из окружения
def test_convert_usd_to_rub(mock_getenv: Mock, mock_get: Mock) -> None:
    """
    ✅ Проверка: при валюте USD вызывается API и возвращается правильная сумма.
    """
    transaction = {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}

    # Мокаем ответ API
    mock_response = Mock()
    mock_response.json.return_value = {"rates": {"RUB": 90.0}}
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response

    result = convert_to_rub(transaction)
    assert result == 9000.0  # 100 * 90
