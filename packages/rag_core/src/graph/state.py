from typing import TypedDict, Literal, NotRequired


class StudyState(TypedDict, total=False):
    # Input (dado por el usuario/API) — semánticamente inmutables tras el inicio
    question: str
    level: str
    module: str | None

    # Router (lo pone classify_intent)
    intent: Literal["teoria", "codigo", "quiz"]

    # CRAG: query reescrita por rewrite_query (question permanece intacta)
    rewritten_query: str | None

    # RAG (lo pone retrieve_context)
    docs: list[dict]

    # Grader y contador de reintentos
    docs_relevant: bool
    retrieval_attempts: int

    # Output del agente especializado
    answer: str
    confidence: float
    related_labs: list[dict]

    # Citas construidas por synthesize_response (vía build_answer_response)
    # Fase 4 podrá leerlas directamente del state si conviene.
    citations: list[dict]

    # Campos estructurados para coder_agent (se llenarán en Fase 3)
    code: str | None
    language: str | None

    # Campos estructurados para quiz_agent (se llenarán en Fase 3)
    quiz_items: list
