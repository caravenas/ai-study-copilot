from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import run_query
from app.services.study_service import StudyOrchestrator, get_orchestrator

router = APIRouter()


@router.post("/", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    orch: StudyOrchestrator = Depends(get_orchestrator),
) -> QueryResponse:
    return await run_in_threadpool(run_query, request, orch)
