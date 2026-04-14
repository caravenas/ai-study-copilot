from fastapi import APIRouter, Depends
from app.schemas.study import StudyRequest
from app.schemas.query import QueryResponse
from app.services.study_service import run_study, run_quiz

from packages.rag_core.src.pipeline import summary_module

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def study_endpoint(request: StudyRequest):
    return await run_study(request)


@router.post("/quiz", response_model=QueryResponse)
async def quiz_endpoint(request: StudyRequest):
    return await run_quiz(request)

@router.get("/summary/{module}", response_model=QueryResponse)
async def summary_endpoint(module: str):
    # Ya que pipeline lo hace derecho, lo saltamos del servicio para ser rápidos
    return summary_module(module)