from unittest.mock import Mock, patch

from src.services import convert_to_rub


def test_convert_rub_no_conversion() -> None:
    """
    ✅ Проверяет, что сумма в RUB возвращается без API-запроса.
    """
    transaction = {"operationAmount": {"amount": "1000.00", "currency": {"code": "RUB"}}}

    result = convert_to_rub(transaction)
    assert result == 1000.0


@patch("src.services.requests.get")
@patch("src.services.os.getenv", return_value="fake-api-key")
def test_convert_usd_to_rub(mock_getenv: Mock, mock_get: Mock) -> None:
    """
    ✅ Проверяет конвертацию USD → RUB с использованием подмены ответа от CurrencyFreaks API.
    """
    # Подделываем ответ API
    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"rates": {"RUB": "90.00"}}
    mock_get.return_value = fake_response

    transaction = {"operationAmount": {"amount": "10.00", "currency": {"code": "USD"}}}

    result = convert_to_rub(transaction)
    assert result == 900.0
    mock_get.assert_called_once()
    assert mock_getenv.called
