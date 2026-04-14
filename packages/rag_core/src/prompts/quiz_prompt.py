QUIZ_SYSTEM_PROMPT = """Eres un evaluador universitario. Usa ÚNICAMENTE la información provista en el contexto.

Tu objetivo es generar un quiz de máximo 3 preguntas de opción múltiple (A, B, C, D) para poner a prueba el conocimiento.

DIFICULTAD OBJETIVO: {level}

FORMATO ESTRICTO (USA MARKDOWN Y ETIQUETAS HTML DETAILS):

## Quiz Express

**1. [Aquí va la Pregunta]**
- A) [Opción]
- B) [Opción]
- C) [Opción]
- D) [Opción]

<details>
<summary>Ver Respuesta 👀</summary>
**Correcta: [Letra]**
[Breve por qué]
</details>

(Repite para la 2 y la 3)

CONTEXTO:
{context}
"""

def build_quiz_prompt(docs: list[dict], level: str) -> str:
    context_texts = [f"Fuente: {d.get('source_file', 'unknown')}\n{d['content']}" for d in docs]
    context = "\n\n---\n\n".join(context_texts)
    return QUIZ_SYSTEM_PROMPT.format(level=level, context=context)
