import logging

from app.schemas.study import StudyRequest
from app.schemas.query import QueryResponse
from app.adapters.state_to_response import to_query_response
from packages.rag_core.src.graph.study_graph import get_study_graph
from packages.rag_core.src.services.retrieval import build_where_filter, retrieve
from packages.rag_core.src.services.agents import run_quiz as run_quiz_agent

logger = logging.getLogger(__name__)


class StudyOrchestrator:
    def __init__(self, graph):
        self._graph = graph

    def run(self, request) -> QueryResponse:
        # Normaliza tanto StudyRequest (tiene level) como QueryRequest (no tiene level).
        initial_state = {
            "question": request.question,
            "level": getattr(request, "level", "intermedio"),
            "module": request.module,
            "difficulty": getattr(request, "difficulty", None),
        }
        final_state = self._graph.invoke(initial_state)
        return to_query_response(final_state)

    def run_as_quiz(self, request: StudyRequest) -> QueryResponse:
        try:
            # Fuerza intent="quiz" para saltarse el clasificador.
            initial_state = {
                "question": request.question,
                "level": request.level,
                "module": request.module,
                "difficulty": request.difficulty,
                "intent": "quiz",
            }
            final_state = self._graph.invoke(initial_state)

            # Fallback defensivo: si por cualquier motivo el grafo no devolvió
            # quiz_items, forzamos generación de quiz para mantener UX de flashcards.
            if not final_state.get("quiz_items"):
                docs = final_state.get("docs") or retrieve(
                    question=request.question,
                    filters=build_where_filter(module=request.module, difficulty=request.difficulty),
                    k=5,
                )
                quiz_result = run_quiz_agent(
                    question=request.question,
                    docs=docs,
                    level=request.level,
                    difficulty=request.difficulty,
                )
                final_state["intent"] = "quiz"
                final_state["docs"] = docs
                final_state["answer"] = quiz_result["answer"]
                final_state["quiz_items"] = quiz_result["quiz_items"]

            return to_query_response(final_state)
        except Exception:
            logger.exception("run_as_quiz failed")
            # Evita cortar el socket en frontend; responde payload válido.
            return QueryResponse(
                answer="No pude generar el quiz en este momento. Reintenta en unos segundos.",
                citations=[],
                related_labs=[],
                confidence=0.0,
                quiz_items=[],
                intent="quiz",
                code=None,
                language=None,
            )


def get_orchestrator() -> StudyOrchestrator:
    return StudyOrchestrator(graph=get_study_graph())


def run_study(request: StudyRequest) -> QueryResponse:
    return get_orchestrator().run(request)


def run_quiz(request: StudyRequest, orch: StudyOrchestrator = None) -> QueryResponse:
    # Fuerza intent="quiz" en el grafo, sin pasar por el clasificador.
    orchestrator = orch or get_orchestrator()
    return orchestrator.run_as_quiz(request)
