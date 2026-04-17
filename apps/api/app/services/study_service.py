from app.schemas.study import StudyRequest
from app.schemas.query import QueryResponse
from packages.rag_core.src.graph.study_graph import study_graph
from packages.rag_core.src.pipeline import quiz_question


async def run_study(request: StudyRequest) -> QueryResponse:
    result = study_graph.invoke({
        "question": request.question,
        "level": request.level,
        "module": request.module,
    })
    return QueryResponse(
        answer=result["answer"],
        citations=result.get("citations", []),
        related_labs=result.get("related_labs", []),
        confidence=result.get("confidence", 0.0),
    )


async def run_quiz(request: StudyRequest) -> QueryResponse:
    # El endpoint /quiz es explícito: siempre genera un quiz sin pasar por el clasificador.
    result = quiz_question(
        question=request.question,
        level=request.level,
        module=request.module,
        difficulty=request.difficulty,
        top_k=4
    )
    return QueryResponse(**result)