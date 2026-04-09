from fastapi import APIRouter
from app.schemas.ingest import IngestRequest, IngestResponse
from app.services.ingest_service import run_ingest

router = APIRouter()

@router.post("/", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest) -> IngestResponse:
    return await run_ingest(request)
