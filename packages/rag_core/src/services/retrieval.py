"""
Servicio de recuperación de documentos.

Encapsula build_where_filter y retrieve_documents para que
pipeline.py y graph/nodes.py consuman desde un único lugar.
"""

from packages.rag_core.src.retrieval.filters import build_where_filter as _build_where_filter
from packages.rag_core.src.retrieval.retriever import retrieve_documents as _retrieve_documents


def build_where_filter(
    module: str | None = None,
    difficulty: str | None = None,
    week: int | None = None,
    course: str | None = None,
) -> dict | None:
    """Proxy directo sobre retrieval.filters.build_where_filter."""
    return _build_where_filter(module=module, difficulty=difficulty, week=week, course=course)


def retrieve(question: str, filters: dict | None, k: int) -> list[dict]:
    """Wrapper sobre retrieve_documents con firma más corta."""
    return _retrieve_documents(question=question, top_k=k, where_filter=filters)
