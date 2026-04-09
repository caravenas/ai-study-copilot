from fastapi import APIRouter
from app.schemas.query import QueryRequest, QueryResponse
from app.services.query_service import run_query

router = APIRouter()

@router.post("/", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest) -> QueryResponse:
    return await run_query(request)
    
