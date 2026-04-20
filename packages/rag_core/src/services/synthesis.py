"""
Servicio de síntesis de respuestas.

Centraliza build_answer_response y find_related_labs para que
pipeline.py y graph/nodes.py los consuman desde un único lugar.
"""

from packages.rag_core.src.synthesis.answer_builder import build_answer_response as _build_answer_response
from packages.rag_core.src.vectorstore.chroma_store import get_notebook_chunks
from packages.rag_core.src.linking.lab_linker import find_related_labs as _find_related_labs


def build_answer_response(answer: str, docs: list[dict], extras: dict | None = None) -> dict:
    """
    Construye la respuesta final con citations y confidence.

    extras permite agregar campos adicionales (e.g. quiz_items, code)
    sin modificar la firma base — útil para fases futuras.
    """
    response = _build_answer_response(answer=answer, docs=docs)
    if extras:
        response.update(extras)
    return response


def find_related_labs(docs: list[dict]) -> list[dict]:
    """
    Busca laboratorios relacionados con los docs recuperados.

    Obtiene los notebook_docs internamente para no exponer esa
    dependencia a los callers (pipeline y nodos del grafo).
    """
    notebook_docs = get_notebook_chunks()
    return _find_related_labs(docs, notebook_docs)
