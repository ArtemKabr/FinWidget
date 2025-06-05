import pytest
from fastapi.testclient import TestClient

from src.main import app


def test_get_operations_filtered_ok(client: TestClient) -> None:
    """
    ✅ Проверяет фильтрацию операций по статусу и валюте.
    """
    response = client.get("/operations", params={"status": "OK", "currency": "RUB"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "operations" in data


def test_get_operations_not_found(client: TestClient) -> None:
    """
    ✅ Проверяет случай, когда ни одна операция не подходит под фильтр.
    """
    response = client.get("/operations", params={"status": "CANCELLED"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("operations"), list)
    assert len(data["operations"]) == 0


def test_get_categories(client: TestClient) -> None:
    """
    ✅ Проверяет, что список категорий возвращается и не пустой.
    """
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data.get("categories"), list)
    assert data["categories"]


@pytest.fixture
def client() -> TestClient:
    """
    🔧 Фикстура для клиента FastAPI.
    """
    return TestClient(app)


def test_get_summary(client: TestClient) -> None:
    """
    ✅ Проверяет, что /summary возвращает общую статистику.
    """
    response = client.get("/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_operations" in data
    assert "by_status" in data
    assert isinstance(data["by_status"], dict)
