from fastapi import APIRouter
from app.schemas.eval import EvalRequest, EvalResponse
from app.services.eval_service import run_eval

router = APIRouter()

@router.post("/", response_model=EvalResponse)
async def eval_endpoint(request: EvalRequest):
    return await run_eval(request)
