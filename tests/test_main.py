from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_add_positive_numbers() -> None:
    response = client.post("/add", json={"a": 3, "b": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 8}

def test_add_negative_and_float() -> None:
    response = client.post("/add", json={"a": -3.0, "b": -5.0})
    assert response.status_code == 200
    assert response.json() == {"result": -8.0}

def test_add_invalid_input_returns_422() -> None:
    response = client.post("/add", json={"a": "invalid", "b": 5})
    assert response.status_code == 422

def test_add_missing_field_returns_422() -> None:
    response = client.post("/add", json={"a": 3})
    assert response.status_code == 422

def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_index_page_renders() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Add Two Numbers" in response.text

def test_add_form_returns_result_fragment() -> None:
    response = client.post("/add-form", data={"a": "3", "b": "5"})
    assert response.status_code == 200
    assert "Result:" in response.text
    assert "8.0" in response.text