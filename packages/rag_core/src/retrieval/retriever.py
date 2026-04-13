from packages.rag_core.src.embeddings.provider import embed_query
from packages.rag_core.src.vectorstore.chroma_store import search_chunks

def retrieve_documents(question: str, top_k: int, where_filter: dict | None = None):
    query_embedding = embed_query(question)
    docs = search_chunks(query_embedding, top_k=top_k, where=where_filter)
    return docs 