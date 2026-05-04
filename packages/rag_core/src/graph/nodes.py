from packages.rag_core.src.llm.client import generate_answer
from packages.rag_core.src.graph.state import StudyState

from packages.rag_core.src.services.retrieval import build_where_filter, retrieve
from packages.rag_core.src.services.synthesis import build_answer_response, find_related_labs
from packages.rag_core.src.services.agents import run_tutor, run_coder, run_quiz


ROUTER_PROMPT = """Clasifica la intención de esta pregunta de un estudiante.

Responde ÚNICAMENTE con una de estas palabras (sin puntos, sin explicación):
- teoria → si pregunta conceptos, definiciones, explicaciones teóricas
- codigo → si pide código, implementación, debugging, o errores de programación
- quiz   → si pide evaluación, quiz, preguntas de práctica o examen

Pregunta: {question}"""


GRADER_PROMPT = """Eres un evaluador de relevancia para un sistema RAG.

Dado el siguiente contexto recuperado y la pregunta del estudiante, determina si el contexto
contiene información relacionada con el tema, aunque sea de forma parcial.

Responde ÚNICAMENTE con una de estas palabras:
- relevante → si el contexto tiene información relacionada con el tema preguntado (aunque sea parcial)
- irrelevante → si el contexto es completamente ajeno al tema preguntado

En caso de duda, responde: relevante

PREGUNTA: {question}

CONTEXTO RECUPERADO:
{context}"""

REWRITE_PROMPT = """Eres un experto en reformulación de queries para búsqueda semántica.

La siguiente pregunta no encontró documentos relevantes. Reescríbela para mejorar la búsqueda.
Usa sinónimos, términos técnicos alternativos o desglosa el concepto.
Responde ÚNICAMENTE con la pregunta reformulada, sin explicación.

PREGUNTA ORIGINAL: {question}"""


def classify_intent(state: StudyState) -> dict:
    """Nodo Router: clasifica la pregunta en una intención."""
    preset_intent = state.get("intent")
    if preset_intent in ("teoria", "codigo", "quiz"):
        # Permite que endpoints especializados (ej. /study/quiz) fuercen ruta.
        return {"intent": preset_intent}

    prompt = ROUTER_PROMPT.format(question=state["question"])
    raw = generate_answer(prompt).strip().lower()

    # Sanitizar: si el LLM devuelve algo inesperado, fallback a "teoria"
    intent = raw if raw in ("teoria", "codigo", "quiz") else "teoria"

    return {"intent": intent}


def retrieve_context(state: StudyState) -> dict:
    """Nodo RAG: busca documentos relevantes en ChromaDB.

    Usa rewritten_query si existe (tras un rewrite_query), de lo contrario
    usa la pregunta original para no perder el intent del usuario.
    """
    where_filter = build_where_filter(module=state.get("module"))
    query = state.get("rewritten_query") or state["question"]
    docs = retrieve(question=query, filters=where_filter, k=5)

    return {"docs": docs}


def tutor_agent(state: StudyState) -> dict:
    """Agente Teórico: explica conceptos al nivel del estudiante."""
    answer = run_tutor(question=state["question"], docs=state["docs"], level=state["level"])
    return {"answer": answer}


def coder_agent(state: StudyState) -> dict:
    """Agente de Código: resuelve preguntas de implementación.

    Retorna answer (Markdown completo), code y language extraídos del
    primer fenced code-block. Si no hay code-block, code y language son None.
    """
    result = run_coder(question=state["question"], docs=state["docs"], level=state["level"])
    return {"answer": result["answer"], "code": result["code"], "language": result["language"]}


def quiz_agent(state: StudyState) -> dict:
    """Agente Quiz: genera evaluaciones interactivas.

    Retorna answer (texto crudo del LLM) y quiz_items (lista parseada).
    Si el parseo JSON falla, quiz_items es [].
    """
    result = run_quiz(question=state["question"], docs=state["docs"], level=state["level"])
    return {"answer": result["answer"], "quiz_items": result["quiz_items"]}


def synthesize_response(state: StudyState) -> dict:
    """Nodo final: ensambla la respuesta con citations y labs."""
    related_labs = find_related_labs(state["docs"])
    response = build_answer_response(state["answer"], state["docs"])
    response["related_labs"] = related_labs
    return response


def grade_documents(state: StudyState) -> dict:
    docs = state["docs"]
    attempts = state.get("retrieval_attempts", 0)

    # Sin docs: irrelevante de inmediato
    if not docs:
        return {"docs_relevant": False, "retrieval_attempts": attempts}

    # Heurística: 3+ docs con contenido sustancial → aceptar sin llamar al LLM
    substantial = [d for d in docs if len(d["content"]) > 100]
    if len(substantial) >= 3:
        return {"docs_relevant": True, "retrieval_attempts": attempts}

    # LLM grader para casos con pocos docs o contenido mixto
    context = "\n\n".join(d["content"] for d in docs)
    prompt = GRADER_PROMPT.format(question=state["question"], context=context)
    raw = generate_answer(prompt).strip().lower()
    return {
        "docs_relevant": "irrelevante" not in raw,
        "retrieval_attempts": attempts,
    }


def rewrite_query(state: StudyState) -> dict:
    """Reformula la query si los docs no fueron relevantes.

    Escribe la versión reescrita en rewritten_query para preservar
    state["question"] como la pregunta original del usuario.
    """
    # Siempre reformula desde la pregunta original, no desde una reescritura previa
    prompt = REWRITE_PROMPT.format(question=state["question"])
    rewritten = generate_answer(prompt).strip()
    return {
        "rewritten_query": rewritten,
        "retrieval_attempts": state.get("retrieval_attempts", 0) + 1,
    }


def handle_no_context(state: StudyState) -> dict:
    """Fallback cuando tras los reintentos no se encontró contexto relevante."""
    return {
        "answer": (
            f"No encontré información suficiente en los materiales del curso "
            f"para responder sobre: '{state['question']}'. "
            f"Intenta reformular la pregunta o verifica que el tema esté en los documentos indexados."
        ),
        "citations": [],
        "confidence": 0.0,
        "related_labs": [],
    }
