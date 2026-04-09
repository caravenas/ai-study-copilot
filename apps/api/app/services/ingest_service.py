from pathlib import Path
from fastapi import HTTPException
from app.schemas.ingest import IngestRequest, IngestResponse
from packages.ingestion.src.pipeline import ingest_pdf, ingest_notebook

# apps/api/app/services/ -> apps/api/app/ -> apps/api/ -> apps/ -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]

INGEST_HANDLERS = {
    ".pdf": ingest_pdf,
    ".ipynb": ingest_notebook,
}

async def run_ingest(request: IngestRequest) -> IngestResponse:
    file_path = request.file_path
    if not Path(file_path).is_absolute():
        file_path = str(PROJECT_ROOT / file_path)

    suffix = Path(file_path).suffix.lower()
    handler = INGEST_HANDLERS.get(suffix)
    if handler is None:
        supported = ", ".join(INGEST_HANDLERS.keys())
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Supported: {supported}",
        )

    result = handler(file_path)
    return IngestResponse(**result)
    