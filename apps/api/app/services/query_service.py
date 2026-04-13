from app.schemas.query import QueryRequest, QueryResponse
from packages.rag_core.src.pipeline import answer_question

async def run_query(request: QueryRequest) -> QueryResponse:
    result = answer_question(
        question=request.question,
        module=request.module,
        difficulty=request.difficulty,
        top_k=request.top_k,
    )
    return QueryResponse(**result)
