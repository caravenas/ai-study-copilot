"""
Servicio de agentes LLM especializados.

Encapsula la lógica de construcción de prompt + llamada al LLM para
los tres agentes (tutor, coder, quiz), eliminando la duplicación entre
pipeline.py y graph/nodes.py.
"""

import json
import logging
import re

from packages.rag_core.src.prompts.study_prompt import build_study_prompt
from packages.rag_core.src.prompts.coder_prompt import build_coder_prompt
from packages.rag_core.src.prompts.quiz_prompt import build_quiz_prompt
from packages.rag_core.src.llm.client import generate_answer

logger = logging.getLogger(__name__)


def _extract_first_code_block(markdown: str) -> tuple[str | None, str | None]:
    """
    Extrae el primer fenced code-block de un string Markdown.

    Retorna (code, language) donde language está normalizado a minúsculas.
    Si no hay code-block, retorna (None, None).
    Si el fence no especifica lenguaje, language=None.
    """
    # Acepta ``` con lenguaje opcional, captura hasta el ``` de cierre
    pattern = re.compile(r"```(\w+)?\n(.*?)```", re.DOTALL)
    match = pattern.search(markdown)
    if not match:
        return None, None
    lang_raw = match.group(1)
    code = match.group(2)
    language = lang_raw.lower() if lang_raw else None
    return code, language


def run_tutor(question: str, docs: list[dict], level: str) -> str:
    """Ejecuta el agente teórico y devuelve el texto de respuesta."""
    sys_prompt = build_study_prompt(docs=docs, level=level)
    user_msg = f"Profesor, tengo esta duda: '{question}'"
    return generate_answer(prompt=user_msg, system_prompt=sys_prompt)


def run_coder(question: str, docs: list[dict], level: str) -> dict:
    """
    Ejecuta el agente de código.

    Retorna {"answer": str, "code": str | None, "language": str | None}.
    answer contiene el Markdown completo; code y language se extraen del
    primer fenced code-block. Si no hay code-block, ambos son None.
    """
    sys_prompt = build_coder_prompt(docs=docs, level=level)
    user_msg = f"Necesito ayuda con: '{question}'"
    answer = generate_answer(prompt=user_msg, system_prompt=sys_prompt)
    code, language = _extract_first_code_block(answer)
    return {"answer": answer, "code": code, "language": language}


def run_quiz(question: str, docs: list[dict], level: str, difficulty: str | None = None) -> dict:
    """
    Ejecuta el agente quiz y parsea el JSON estructurado.

    Retorna {"answer": str, "quiz_items": list}.
    answer contiene el texto crudo del LLM para trazabilidad.
    quiz_items contiene los items parseados; si el parseo falla, es [].

    Busca el primer '[' y el último ']' para extraer el bloque JSON,
    preservando la lógica robusta original.
    """
    # difficulty no se usa en build_quiz_prompt pero se recibe para
    # mantener la firma alineada con la especificación de Fase 1.
    sys_prompt = build_quiz_prompt(docs=docs, level=level)
    user_msg = f"Hazme un quiz de 3 preguntas sobre: '{question}'"
    llm_answer = generate_answer(prompt=user_msg, system_prompt=sys_prompt)

    quiz_items: list = []
    try:
        start = llm_answer.find("[")
        end = llm_answer.rfind("]") + 1
        if start != -1:
            quiz_items = json.loads(llm_answer[start:end])
    except (json.JSONDecodeError, ValueError):
        logger.warning("run_quiz: no se pudo parsear JSON de quiz_items; se devuelve lista vacía.")

    return {"answer": llm_answer, "quiz_items": quiz_items}
