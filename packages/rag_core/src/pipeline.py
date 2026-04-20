from packages.rag_core.src.services.retrieval import build_where_filter, retrieve
from packages.rag_core.src.services.synthesis import build_answer_response, find_related_labs
from packages.rag_core.src.services.agents import run_quiz

from packages.rag_core.src.prompts.answer_prompt import build_answer_prompt
from packages.rag_core.src.prompts.study_prompt import build_study_prompt
from packages.rag_core.src.prompts.summary_prompt import build_summary_prompt
from packages.rag_core.src.llm.client import generate_answer

from packages.rag_core.src.vectorstore.chroma_store import get_module_chunks
from packages.rag_core.src.retrieval.retriever import retrieve_documents


def answer_question(question: str, module: str | None = None, difficulty: str | None = None, top_k: int = 4) -> dict:
    where_filter = build_where_filter(module=module, difficulty=difficulty)
    docs = retrieve(question=question, filters=where_filter, k=top_k)

    if not docs:
        return build_answer_response(
            answer="No encontré información suficiente en los documentos para responder a esta pregunta.",
            docs=[],
        )

    prompt = build_answer_prompt(question=question, docs=docs)
    llm_answer = generate_answer(prompt)

    related_labs = find_related_labs(docs)

    response = build_answer_response(llm_answer, docs)
    response["related_labs"] = related_labs

    return response


def study_question(question: str, level: str = "intermedio", module: str | None = None, difficulty: str | None = None, top_k: int = 4) -> dict:
    where_filter = build_where_filter(module=module, difficulty=difficulty)
    docs = retrieve(question=question, filters=where_filter, k=top_k)

    if not docs:
        return build_answer_response(
            answer="No encontré información suficiente en los documentos para armar una tutoría.",
            docs=[],
        )

    # 1. Armamos el "cerebro" (System Prompt) con los documentos RAG y el nivel elegido
    study_sys_prompt = build_study_prompt(docs=docs, level=level)

    # 2. El usuario solo hace la pregunta (user_prompt distinto al del nodo del grafo)
    user_prompt = f"Profesor, tengo esta duda: '{question}'. Explícamelo a mi nivel y déjame preguntas de repaso."

    # 3. Disparamos la generación
    llm_answer = generate_answer(prompt=user_prompt, system_prompt=study_sys_prompt)

    # 4. Vínculo cruzado entre PDFs y Notebooks
    related_labs = find_related_labs(docs)

    response = build_answer_response(llm_answer, docs)
    response["related_labs"] = related_labs

    return response


def quiz_question(question: str, level: str = "intermedio", module: str | None = None, difficulty: str | None = None, top_k: int = 4) -> dict:
    where_filter = build_where_filter(module=module, difficulty=difficulty)
    docs = retrieve(question=question, filters=where_filter, k=top_k)

    if not docs:
        return build_answer_response(answer="No hay suficiente contexto para armar un quiz de esto.", docs=[])

    quiz_result = run_quiz(question=question, docs=docs, level=level, difficulty=difficulty)
    llm_answer = quiz_result["answer"]
    quiz_items = quiz_result["quiz_items"]

    related_labs = find_related_labs(docs)

    response = build_answer_response(llm_answer, docs)
    response["related_labs"] = related_labs
    response["quiz_items"] = quiz_items

    return response


def summary_module(module: str) -> dict:
    # 1. Intento exacto por metadato module
    docs = get_module_chunks(module)

    # 2. Fallback semántico si no hubo match exacto
    if not docs:
        docs = retrieve_documents(question=module, top_k=10)

    if not docs:
        return build_answer_response(
            answer=f"No hay suficiente contexto para armar un resumen del módulo: '{module}'.", docs=[]
        )

    summary_sys_prompt = build_summary_prompt(docs=docs, module=module)
    user_prompt = "Genera el súper resumen de todo este contenido del módulo."
    llm_answer = generate_answer(prompt=user_prompt, system_prompt=summary_sys_prompt)

    return build_answer_response(llm_answer, docs[:5])
