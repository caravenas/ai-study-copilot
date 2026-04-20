from app.schemas.study import StudyRequest
from app.schemas.query import QueryResponse
from app.adapters.state_to_response import to_query_response
from packages.rag_core.src.graph.study_graph import get_study_graph


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
        # Fuerza intent="quiz" para saltarse el clasificador.
        initial_state = {
            "question": request.question,
            "level": request.level,
            "module": request.module,
            "difficulty": request.difficulty,
            "intent": "quiz",
        }
        final_state = self._graph.invoke(initial_state)
        return to_query_response(final_state)


def get_orchestrator() -> StudyOrchestrator:
    return StudyOrchestrator(graph=get_study_graph())


async def run_study(request: StudyRequest) -> QueryResponse:
    return get_orchestrator().run(request)


async def run_quiz(request: StudyRequest, orch: StudyOrchestrator = None) -> QueryResponse:
    # Fuerza intent="quiz" en el grafo, sin pasar por el clasificador.
    orchestrator = orch or get_orchestrator()
    return orchestrator.run_as_quiz(request)
