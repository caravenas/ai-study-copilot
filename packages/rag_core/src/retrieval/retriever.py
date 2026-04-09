from packages.rag_core.src.embeddings.provider import embed_query
from packages.rag_core.src.vectorstore.chroma_store import search_chunks

def retrieve_documents(question: str, top_k: int):
    query_embedding = embed_query(question)
    return search_chunks(query_embedding=query_embedding, top_k=top_k)