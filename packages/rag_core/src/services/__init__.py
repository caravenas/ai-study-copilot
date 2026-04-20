"""
Paquete de servicios compartidos del rag_core.

Expone las funciones públicas de retrieval, synthesis y agents
para que pipeline.py y graph/nodes.py los consuman desde un único lugar.
"""

from packages.rag_core.src.services.retrieval import build_where_filter, retrieve
from packages.rag_core.src.services.synthesis import build_answer_response, find_related_labs
from packages.rag_core.src.services.agents import run_tutor, run_coder, run_quiz

__all__ = [
    "build_where_filter",
    "retrieve",
    "build_answer_response",
    "find_related_labs",
    "run_tutor",
    "run_coder",
    "run_quiz",
]
