from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_operations_filtered_ok() -> None:
    """
    ✅ Проверяет фильтрацию операций по статусу и валюте.
    """
    response = client.get("/operations", params={"status": "OK", "currency": "RUB"})
    assert response.status_code == 200
    data = response.json()
    assert "operations" in data
    assert isinstance(data["operations"], list)
    for item in data["operations"]:
        assert item["Статус"] == "OK"
        assert item["Валюта операции"] == "RUB"


def test_get_operations_not_found() -> None:
    """
    ✅ Проверяет случай, когда ни одна операция не подходит под фильтр.
    """
    response = client.get("/operations", params={"status": "CANCELLED"})
    assert response.status_code == 200
    data = response.json()
    assert data["operations"] == []
