"""
Tests de POST /api/query/ — Fase 7.

El endpoint delega siempre al orquestador (grafo). No hay fallback legacy.
"""
from app.core.config import settings


QUERY_PAYLOAD = {
    "question": "¿Qué es una red neuronal?",
    "module": None,
    "difficulty": None,
    "top_k": 5,
}


def test_query_usa_grafo(client_with_fake_orch):
    """El endpoint delega al FakeOrchestrator inyectado y la respuesta viene del grafo."""
    response = client_with_fake_orch.post("/api/query/", json=QUERY_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    # El FakeOrchestrator devuelve "respuesta-fake"
    assert data["answer"] == "respuesta-fake"
    # Los tres campos nuevos deben estar presentes (pueden ser None)
    assert "intent" in data
    assert "code" in data
    assert "language" in data
    assert data["intent"] == "teoria"
