from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.ingest import IngestRequest, IngestResponse, SourceItem
from app.services.ingest_service import run_ingest, save_upload_and_ingest, list_sources

from packages.rag_core.src.vectorstore.chroma_store import get_sources_summary

router = APIRouter()

@router.post("/", response_model=IngestResponse)
async def ingest_endpoint(request: IngestRequest) -> IngestResponse:
    return await run_ingest(request)

@router.post("/upload", response_model=IngestResponse)
async def upload_endpoint(file: UploadFile = File(...)) -> IngestResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    suffix = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if suffix not in ("pdf", "ipynb"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '.{suffix}'. Supported: .pdf, .ipynb",
        )

    return await save_upload_and_ingest(file)

@router.get("/sources")
async def list_sources():
    """Retorna todas las fuentes indexadas y la cantidad de chunks generados por cada una."""
    sources = get_sources_summary()
    return {"sources": sources, "total_files": len(sources)}

    

