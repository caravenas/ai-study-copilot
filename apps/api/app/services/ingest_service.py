from pathlib import Path
from fastapi import HTTPException, UploadFile
from app.schemas.ingest import IngestRequest, IngestResponse, SourceItem
from packages.ingestion.src.pipeline import ingest_pdf, ingest_notebook
from packages.rag_core.src.vectorstore.chroma_store import collection

# apps/api/app/services/ -> apps/api/app/ -> apps/api/ -> apps/ -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[4]

INGEST_HANDLERS = {
    ".pdf": ingest_pdf,
    ".ipynb": ingest_notebook,
}

# Mapping file extension -> raw data subdirectory
RAW_DIRS = {
    ".pdf": PROJECT_ROOT / "data" / "raw" / "pdfs",
    ".ipynb": PROJECT_ROOT / "data" / "raw" / "notebooks",
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


async def save_upload_and_ingest(file: UploadFile) -> IngestResponse:
    """Save an uploaded file to data/raw/ and run ingestion."""
    suffix = Path(file.filename).suffix.lower()
    raw_dir = RAW_DIRS.get(suffix)

    if raw_dir is None:
        raise HTTPException(status_code=400, detail=f"Unsupported type: {suffix}")

    raw_dir.mkdir(parents=True, exist_ok=True)
    dest = raw_dir / file.filename
    
    content = await file.read()
    dest.write_bytes(content)

    handler = INGEST_HANDLERS[suffix]
    result = handler(str(dest))
    return IngestResponse(**result)


def list_sources() -> list[SourceItem]:
    """List unique source files from the vector store."""
    all_meta = collection.get(include=["metadatas"])
    
    source_map: dict[str, dict] = {}
    for meta in all_meta["metadatas"]:
        sf = meta.get("source_file", "unknown")
        if sf not in source_map:
            source_map[sf] = {
                "source_file": sf,
                "source_type": meta.get("source_type", "unknown"),
                "chunks_count": 0,
            }
        source_map[sf]["chunks_count"] += 1

    return [SourceItem(**v) for v in source_map.values()]