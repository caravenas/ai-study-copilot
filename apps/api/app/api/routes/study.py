from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool
from app.schemas.study import StudyRequest
from app.schemas.query import QueryResponse
from app.services.study_service import StudyOrchestrator, get_orchestrator, run_quiz

from packages.rag_core.src.pipeline import summary_module

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def study_endpoint(
    request: StudyRequest,
    orch: StudyOrchestrator = Depends(get_orchestrator),
):
    return orch.run(request)


@router.post("/quiz", response_model=QueryResponse)
async def quiz_endpoint(request: StudyRequest):
    return await run_quiz(request)


@router.get("/summary/{module}", response_model=QueryResponse)
async def summary_endpoint(module: str):
    # summary_module es bloqueante; se ejecuta en threadpool para no bloquear el event loop.
    return await run_in_threadpool(summary_module, module)
