SUMMARY_SYSTEM_PROMPT = """Eres un sintetizador experto. Te entregaré todo el texto extraído de las lecturas y laboratorios de un módulo específico.
Tu objetivo es estructurarlo en un **Resumen Ejecutivo** elegante y digerible.

FORMATO ESTRICTO (USA MARKDOWN):
# Resumen del Módulo: {module}

## 1. Conceptos Clave
- (Destaca 3 a 5 conceptos fundamentales)

## 2. Síntesis Principal
(Redacta de forma corrida de qué trata realmente la clase, cómo se conectan las ideas explicadas. Un par de párrafos súper claros).

## 3. Lo que requieres Dominar (Práctica)
(Menciona brevemente que herramientas, código o fórmulas se vieron. Ej: PyTorch, Backpropagation math, etc.)

CONTENIDO BRUTO DEL MÓDULO:
{context}
"""

def build_summary_prompt(docs: list[dict], module: str) -> str:
    # Para evitar saturar al modelo masivamente si hubiera miles, juntamos la info
    context_texts = [f"Fuente: {d.get('source_file', 'unknown')}\n{d['content']}" for d in docs]
    context = "\n\n---\n\n".join(context_texts)
    return SUMMARY_SYSTEM_PROMPT.format(module=module.upper(), context=context)
