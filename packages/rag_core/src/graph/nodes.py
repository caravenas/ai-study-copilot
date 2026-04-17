from packages.rag_core.src.llm.client import generate_answer
from packages.rag_core.src.graph.state import StudyState

from packages.rag_core.src.retrieval.retriever import retrieve_documents
from packages.rag_core.src.retrieval.filters import build_where_filter

from packages.rag_core.src.prompts.study_prompt import build_study_prompt
from packages.rag_core.src.prompts.coder_prompt import build_coder_prompt
from packages.rag_core.src.prompts.quiz_prompt import build_quiz_prompt

from packages.rag_core.src.synthesis.answer_builder import build_answer_response
from packages.rag_core.src.vectorstore.chroma_store import get_notebook_chunks
from packages.rag_core.src.linking.lab_linker import find_related_labs


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
    prompt = ROUTER_PROMPT.format(question=state["question"])
    raw = generate_answer(prompt).strip().lower()

    # Sanitizar: si el LLM devuelve algo inesperado, fallback a "teoria"
    intent = raw if raw in ("teoria", "codigo", "quiz") else "teoria"

    return {"intent": intent}
    
def retrieve_context(state: StudyState) -> dict:
    """Nodo RAG: busca documentos relevantes en ChromaDB."""
    where_filter = build_where_filter(module=state.get("module"))
    docs = retrieve_documents(question=state["question"],top_k=5, where_filter=where_filter)
    
    return {"docs": docs}

def tutor_agent(state: StudyState) -> dict:
    """Agente Teórico: explica conceptos al nivel del estudiante."""
    sys_prompt = build_study_prompt(docs=state["docs"], level=state["level"])
    user_msg = f"Profesor, tengo esta duda: '{state['question']}'"
    answer = generate_answer(prompt=user_msg, system_prompt=sys_prompt)
    return {"answer": answer}


def coder_agent(state: StudyState) -> dict:
    """Agente de Código: resuelve preguntas de implementación."""
    sys_prompt = build_coder_prompt(docs=state["docs"], level=state["level"])
    user_msg = f"Necesito ayuda con: '{state['question']}'"
    answer = generate_answer(prompt=user_msg, system_prompt=sys_prompt)
    return {"answer": answer}

def quiz_agent(state: StudyState) -> dict:
    """Agente Quiz: genera evaluaciones interactivas."""
    sys_prompt = build_quiz_prompt(docs=state["docs"], level=state["level"])
    user_msg = f"Hazme un quiz de 3 preguntas sobre: '{state['question']}'"
    answer = generate_answer(prompt=user_msg, system_prompt=sys_prompt)
    return {"answer": answer}


def synthesize_response(state: StudyState) -> dict:
    """Nodo final: ensambla la respuesta con citations y labs."""
    notebook_docs = get_notebook_chunks()
    related_labs = find_related_labs(state["docs"], notebook_docs)
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
    """Reformula la query si los docs no fueron relevantes."""
    prompt = REWRITE_PROMPT.format(question=state["question"])
    new_question = generate_answer(prompt).strip()
    return {
        "question": new_question,
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
