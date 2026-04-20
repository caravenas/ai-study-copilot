"""
conftest.py — fixtures compartidos para los tests de la API.

Demuestra el patrón de override de dependencias FastAPI:
  app.dependency_overrides[get_orchestrator] = lambda: FakeOrchestrator()

Con esto, los tests de /study nunca tocan Chroma/OpenAI.
"""
import sys
from pathlib import Path

# Asegura que `packages.*` e `app.*` resuelvan desde el monorepo.
_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_root))

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.services.study_service import StudyOrchestrator, get_orchestrator
from app.schemas.query import QueryResponse


class FakeOrchestrator(StudyOrchestrator):
    """Orquestador falso que devuelve una respuesta fija sin llamar al grafo."""

    def __init__(self):
        # No llamamos super().__init__ para no construir el grafo real.
        pass

    def run(self, request) -> QueryResponse:
        return QueryResponse(
            answer="respuesta-fake",
            citations=[],
            related_labs=[],
            confidence=1.0,
            quiz_items=[],
            intent="teoria",
            code=None,
            language=None,
        )


@pytest.fixture()
def client_with_fake_orch():
    """TestClient con el orquestador reemplazado por el fake."""
    app = create_app()
    app.dependency_overrides[get_orchestrator] = lambda: FakeOrchestrator()
    with TestClient(app) as client:
        yield client
    # Limpia overrides al terminar el test.
    app.dependency_overrides.clear()
