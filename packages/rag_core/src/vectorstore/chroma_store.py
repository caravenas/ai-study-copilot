import os
import chromadb

CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/indexes/chroma")
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

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

def search_chunks(query_embedding: list[float], top_k: int = 4) -> list[dict]:
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas"],
    )

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