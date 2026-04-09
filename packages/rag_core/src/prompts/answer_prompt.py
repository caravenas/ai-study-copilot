def build_answer_prompt(question: str, docs: list[dict]) -> str:
    context_blocks = []

    for i, d in enumerate(docs, start=1):
        context_blocks.append(
            f"[{i}] (Fuente: {d['source_file']} pág{d.get('page', 'N/A')})\n{d['content']}"
        )
    
    context = "\n\n".join(context_blocks)

    return f"""
    
Eres un tutor experto en inteligencia artificial.

INSTRUCCIONES CRÍTICAS:
- Responde ÚNICAMENTE basándote en el contexto proporcionado.
- No inventes información que no esté en el contexto.
- Si no encuentras la respuesta en el contexto, responde: "No encontré información suficiente en los documentos para responder a esta pregunta."
- Mantén un tono académico, claro y conciso.
- Usa ejemplos si es útil

FORMATO:
1. Explicación clara
2. Conceptos clave (bullet points)
3. Referencias a fuentes [0], [1], etc.

PREGUNTA:
{question}

CONTEXTO:
{context}
""".strip()


    
    
    