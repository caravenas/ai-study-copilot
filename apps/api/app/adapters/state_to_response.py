"""
Adapter: StudyState → QueryResponse

Convierte el dict final que devuelve el grafo LangGraph en el modelo
Pydantic de la API. El grafo permanece agnóstico de Pydantic/HTTP;
esta capa es la única que conoce ambos lados.
"""

from app.schemas.query import CitationItem, QueryResponse, RelatedLab, QuizItem
from packages.rag_core.src.services.synthesis import build_answer_response, find_related_labs


def to_query_response(state: dict) -> QueryResponse:
    """Convierte el state final del grafo en un QueryResponse HTTP."""
    answer = state.get("answer", "")
    docs = state.get("docs", [])

    # citations y confidence se calculan desde build_answer_response si no
    # fueron puestas en el state por synthesize_response / handle_no_context.
    if "citations" in state and "confidence" in state:
        raw_citations = state["citations"]
        confidence = state["confidence"]
    else:
        base = build_answer_response(answer=answer, docs=docs)
        raw_citations = base["citations"]
        confidence = base["confidence"]

    # related_labs: puede venir del state (handle_no_context las pone vacías,
    # synthesize_response las calcula). Si no está, las calculamos aquí.
    if "related_labs" in state:
        raw_related = state["related_labs"]
    else:
        raw_related = find_related_labs(docs)

    citations = [
        CitationItem(
            source_file=c["source_file"],
            page=c.get("page"),
            chunk_id=c.get("chunk_id", "unknown"),
            excerpt=c["excerpt"],
        )
        for c in raw_citations
    ]

    related_labs = [
        RelatedLab(
            source_file=r["source_file"],
            topics=r.get("topics", []),
            preview=r.get("preview", ""),
        )
        for r in raw_related
    ]

    raw_quiz = state.get("quiz_items") or []
    quiz_items = [
        QuizItem(
            question=q["question"],
            options=q["options"],
            correct=q["correct"],
            explanation=q["explanation"],
        )
        for q in raw_quiz
    ]

    return QueryResponse(
        answer=answer,
        citations=citations,
        related_labs=related_labs,
        confidence=confidence,
        quiz_items=quiz_items,
        intent=state.get("intent"),
        code=state.get("code"),
        language=state.get("language"),
    )
