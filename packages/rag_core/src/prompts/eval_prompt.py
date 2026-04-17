EVAL_PROMPT = """Eres un evaluador experto de sistemas RAG. Evalúa la calidad de esta respuesta.

PREGUNTA DEL ESTUDIANTE:
{question}

DOCUMENTOS RECUPERADOS:
{context}

RESPUESTA GENERADA:
{generated_answer}

RESPUESTA ESPERADA (ground truth):
{expected_answer}

Evalúa las siguientes métricas en escala 0.0 a 1.0 y responde ÚNICAMENTE con JSON válido:

{{
  "retrieval_score": {{
    "score": <float>,
    "reasoning": "<por qué ese puntaje>"
  }},
  "grounding_score": {{
    "score": <float>,
    "reasoning": "<por qué ese puntaje>"
  }},
  "answer_relevance": {{
    "score": <float>,
    "reasoning": "<por qué ese puntaje>"
  }}
}}

Criterios:
- retrieval_score: ¿Los documentos recuperados contienen info relevante para responder la pregunta?
- grounding_score: ¿La respuesta generada se apoya en los documentos? (no alucina)
- answer_relevance: ¿La respuesta generada responde lo que se preguntó, comparada con el ground truth?"""


def build_eval_prompt(question: str, docs: list[dict], generated_answer: str, expected_answer: str) -> str:
    context = "\n\n---\n\n".join(
        f"[{d.get('source_file', 'unknown')}]:\n{d['content']}" for d in docs
    )
    return EVAL_PROMPT.format(
        question=question,
        context=context,
        generated_answer=generated_answer,
        expected_answer=expected_answer,
    )
