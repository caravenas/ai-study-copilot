from packages.ingestion.src.loaders.pdf_loader import load_pdf
from packages.ingestion.src.chunking.pdf_chunker import chunk_pdf_document
from packages.rag_core.src.embeddings.provider import embed_texts
from packages.rag_core.src.vectorstore.chroma_store import add_chunks
from packages.ingestion.src.metadata.enrich import enrich_chunks
from packages.ingestion.src.chunking.notebook_chunker import chunk_notebook
from packages.ingestion.src.parsers.ipynb_parser import parse_notebook


def ingest_pdf(file_path: str) -> dict:
    pages = load_pdf(file_path)
    chunks = chunk_pdf_document(pages, file_path)

    if not chunks:
        return {"status": "empty", "chunks_indexed": 0, "file_path": file_path}

    chunks = enrich_chunks(chunks, {"source_type": "pdf"})

    embeddings = embed_texts([c["content"] for c in chunks])
    add_chunks(chunks, embeddings)

    return {
        "status": "ok",
        "chunks_indexed": len(chunks),
        "file_path": file_path,
    }

def ingest_notebook(file_path: str) -> dict:
    cells = parse_notebook(file_path)
    chunks = chunk_notebook(cells, file_path)

    chunks = enrich_chunks(chunks, {"source_type": "notebook"})

    embeddings = embed_texts([c["content"] for c in chunks])
    add_chunks(chunks, embeddings)

    return {
        "status": "ok",
        "chunks_indexed": len(chunks),
        "file_path": file_path,
    }
    
