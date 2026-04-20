"""
Servicio de generación de resúmenes de módulo.

Extraído de pipeline.py en Fase 7 — único caller era routes/study.py.
"""

from packages.rag_core.src.services.synthesis import build_answer_response
from packages.rag_core.src.retrieval.retriever import retrieve_documents
from packages.rag_core.src.vectorstore.chroma_store import get_module_chunks
from packages.rag_core.src.prompts.summary_prompt import build_summary_prompt
from packages.rag_core.src.llm.client import generate_answer


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
