from app.schemas.query import QueryRequest, QueryResponse
from app.core.config import settings
from packages.rag_core.src.pipeline import answer_question


def run_query(request: QueryRequest, orchestrator=None) -> QueryResponse:
    if settings.USE_GRAPH_FOR_QUERY and orchestrator is not None:
        return orchestrator.run(request)
    # Fallback legacy — Fase 7 retira esta rama.
    result = answer_question(
        question=request.question,
        module=request.module,
        difficulty=request.difficulty,
        top_k=request.top_k,
    )
    return QueryResponse(**result)
