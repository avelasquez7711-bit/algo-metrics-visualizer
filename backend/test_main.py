from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_benchmark():
    payload = {"algorithm": "quick_sort", "distribution": "random", "size": 100}
    response = client.post("/api/benchmark", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "time_ms" in data
    assert "peak_memory_kb" in data
