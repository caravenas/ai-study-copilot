import os
import chromadb

CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/indexes/chroma")
COLLECTION_NAME = "study_materials"

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

def add_chunks(chunks: list[dict], embeddings: list[list[float]]) -> None:
    ids = [c["id"] for c in chunks]
    documents = [c["content"] for c in chunks]
    metadatas = [
        {
            "source_file": c["source_file"],
            "page": c["page"],
        }
        for c in chunks
    ]

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
        docs.append({
            "chunk_id": chunk_id,
            "content": doc,
            "source_file": meta.get("source_file"),
            "page": meta.get("page"),
        })

    return docs