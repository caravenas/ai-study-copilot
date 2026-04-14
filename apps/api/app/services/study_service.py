from app.schemas.study import StudyRequest
from app.schemas.query import QueryResponse
from packages.rag_core.src.pipeline import study_question, quiz_question



async def run_study(request: StudyRequest) -> QueryResponse:
    # Llamamos a nuestro pipeline RAG recién creado
    result = study_question(
        question=request.question,
        level=request.level,
        module=request.module,
        difficulty=request.difficulty,
        top_k=4
    )

    # Como StudyMode devuelve la misma estructura visual (Answer + Citations), 
    # reusamos el QueryResponse del front-end.
    return QueryResponse(**result)

async def run_quiz(request: StudyRequest) -> QueryResponse:
    result = quiz_question(
        question=request.question,
        level=request.level,
        module=request.module,
        difficulty=request.difficulty,
        top_k=4
    )

    return QueryResponse(**result)