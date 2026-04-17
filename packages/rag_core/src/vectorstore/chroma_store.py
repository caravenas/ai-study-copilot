import os
import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[4]
DEFAULT_CHROMA_PATH = str(BASE_DIR / "data" / "indexes" / "chroma")

CHROMA_PATH = os.getenv("CHROMA_PATH", DEFAULT_CHROMA_PATH)
COLLECTION_NAME = "study_materials"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def _build_metadata(chunk: dict) -> dict:
    """Build a ChromaDB-compatible metadata dict from a chunk.
    
    Excludes 'id' and 'content' (stored separately) and any values
    that are not scalar (ChromaDB only supports str, int, float, bool).
    """
    skip_keys = {"id", "content"}
    meta = {}
    for k, v in chunk.items():
        if k in skip_keys:
            continue
        if isinstance(v, (str, int, float, bool)):
            meta[k] = v
        elif isinstance(v, list):
            # Serialize lists as comma-separated strings
            meta[k] = ", ".join(str(item) for item in v)
    return meta

def add_chunks(chunks: list[dict], embeddings: list[list[float]]) -> None:
    ids = [c["id"] for c in chunks]
    documents = [c["content"] for c in chunks]
    metadatas = [_build_metadata(c) for c in chunks]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

def search_chunks(query_embedding: list[float], top_k: int = 4, where: dict | None = None) -> list[dict]:
    count = collection.count()
    if count == 0:
        return []

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": min(top_k, count),
        "include": ["documents", "metadatas"],
    }

    if where:
        query_kwargs["where"] = where
    result = collection.query(**query_kwargs)

    docs = []
    ids = result["ids"][0]
    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    for chunk_id, doc, meta in zip(ids, documents, metadatas):
        entry = {
            "chunk_id": chunk_id,
            "content": doc,
            **meta,
        }
        # Deserialize comma-separated topics back to list
        if "topics" in entry and isinstance(entry["topics"], str):
            entry["topics"] = [t.strip() for t in entry["topics"].split(",") if t.strip()]
        docs.append(entry)

    return docs


def get_notebook_chunks() -> list[dict]:
    """Retrieve all chunks with source_type='notebook' from the collection."""
    result = collection.get(
        where={"source_type": "notebook"},
        include=["documents", "metadatas"],
    )

    docs = []
    for chunk_id, doc, meta in zip(result["ids"], result["documents"], result["metadatas"]):
        entry = {
            "chunk_id": chunk_id,
            "content": doc,
            **meta,
        }
        if "topics" in entry and isinstance(entry["topics"], str):
            entry["topics"] = [t.strip() for t in entry["topics"].split(",") if t.strip()]
        docs.append(entry)

    return docs

def get_sources_summary() -> list[dict]:
    """Devuelve un listado de todas las fuentes indexadas únicas y su conteo de chunks."""
    # Obtenemos TODOS los metadatos directamente del índice vectorial
    result = collection.get(include=["metadatas"])
    metadatas = result["metadatas"]
    
    sources = {}
    for m in metadatas:
        src = m.get("source_file", "Desconocido")
        if src not in sources:
            sources[src] = {
                "source_file": src,
                "source_type": m.get("source_type", ""),
                "module": m.get("module", ""),
                "chunk_count": 0
            }
        sources[src]["chunk_count"] += 1
    
    return list(sources.values())

def get_module_chunks(module_slug: str) -> list[dict]:
    """Retrieve all chunks matching exactly a specific module."""
    result = collection.get(
        where={"module": module_slug},
        include=["documents", "metadatas"]
    )
    
    docs = []
    if not result["ids"]:
        return docs
        
    for chunk_id, doc, meta in zip(result["ids"], result["documents"], result["metadatas"]):
        entry = {
            "chunk_id": chunk_id,
            "content": doc,
            **meta,
        }
        docs.append(entry)
    return docs


    