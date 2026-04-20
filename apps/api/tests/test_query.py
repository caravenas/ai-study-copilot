"""
Tests de POST /api/query/ — Fase 6.

Test 1: con flag activo, el endpoint delega al FakeOrchestrator (no toca el pipeline).
Test 2: con flag desactivado, el endpoint cae al fallback legacy (pipeline mockeado).
"""
import pytest
from unittest.mock import patch

from app.core.config import settings


QUERY_PAYLOAD = {
    "question": "¿Qué es una red neuronal?",
    "module": None,
    "difficulty": None,
    "top_k": 5,
}

LEGACY_RESULT = {
    "answer": "respuesta-legacy",
    "citations": [],
    "related_labs": [],
    "confidence": 0.8,
    "quiz_items": [],
    "intent": None,
    "code": None,
    "language": None,
}


def test_query_usa_grafo(client_with_fake_orch):
    """Con USE_GRAPH_FOR_QUERY=True y FakeOrchestrator inyectado, la respuesta viene del fake."""
    with patch.object(settings, "USE_GRAPH_FOR_QUERY", True):
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


def test_query_fallback_legacy(client_with_fake_orch):
    """Con USE_GRAPH_FOR_QUERY=False, el endpoint usa el pipeline legacy (mockeado)."""
    with patch.object(settings, "USE_GRAPH_FOR_QUERY", False):
        with patch(
            "app.services.query_service.answer_question",
            return_value=LEGACY_RESULT,
        ) as mock_pipeline:
            response = client_with_fake_orch.post("/api/query/", json=QUERY_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "respuesta-legacy"
    assert "intent" in data
    assert "code" in data
    assert "language" in data
    # Verifica que se invocó el pipeline legacy, no el orquestador.
    mock_pipeline.assert_called_once()
