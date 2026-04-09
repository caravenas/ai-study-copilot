from pathlib import Path
from app.schemas.ingest import IngestRequest, IngestResponse
from packages.ingestion.src.pipeline import ingest_pdf

# apps/api/app/services/ -> apps/api/app/ -> apps/api/ -> apps/ -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]

async def run_ingest(request: IngestRequest) -> IngestResponse:
    file_path = request.file_path
    if not Path(file_path).is_absolute():
        file_path = str(PROJECT_ROOT / file_path)
    result = ingest_pdf(file_path)
    return IngestResponse(**result)
    