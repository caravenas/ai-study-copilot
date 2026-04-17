QUIZ_SYSTEM_PROMPT = """Eres un evaluador universitario. Usa ÚNICAMENTE la información provista en el contexto.

Genera exactamente 3 preguntas de opción múltiple (A, B, C, D).

Responde ÚNICAMENTE con un array JSON válido, sin texto adicional, sin markdown, sin explicación:

[
  {{
    "question": "Texto de la pregunta",
    "options": ["A) Opción uno", "B) Opción dos", "C) Opción tres", "D) Opción cuatro"],
    "correct": "B",
    "explanation": "Breve explicación de por qué es correcta"
  }}
]

DIFICULTAD: {level}

CONTEXTO:
{context}
"""


def build_quiz_prompt(docs: list[dict], level: str) -> str:
    context_texts = [f"Fuente: {d.get('source_file', 'unknown')}\n{d['content']}" for d in docs]
    context = "\n\n---\n\n".join(context_texts)
    return QUIZ_SYSTEM_PROMPT.format(level=level, context=context)
