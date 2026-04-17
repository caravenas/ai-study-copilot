from typing import TypedDict, Literal

class StudyState(TypedDict):
    # Input (dado por el Usuario/API)
    question: str
    level: str
    module: str | None

    # Router(lo pone el nodo clasificador)
    intent: Literal["teoria", "codigo", "quiz"]

    # RAG (lo pone el nodo de retrieval)
    docs: list[dict]

    # NUEVO: resultado del grader y contador de reintentos
    docs_relevant: bool
    retrieval_attempts: int

    # Output (lo pone el agente especializado)
    answer: str
    citations: list[dict]
    confidence: float
    related_labs: list[dict]

    