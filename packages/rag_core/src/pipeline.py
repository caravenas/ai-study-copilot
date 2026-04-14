from packages.rag_core.src.retrieval.retriever import retrieve_documents
from packages.rag_core.src.prompts.answer_prompt import build_answer_prompt
from packages.rag_core.src.synthesis.answer_builder import build_answer_response
from packages.rag_core.src.llm.client import generate_answer
from packages.rag_core.src.vectorstore.chroma_store import get_notebook_chunks

from packages.rag_core.src.linking.lab_linker import find_related_labs
from packages.rag_core.src.retrieval.filters import build_where_filter

from packages.rag_core.src.prompts.study_prompt import build_study_prompt
from packages.rag_core.src.prompts.quiz_prompt import build_quiz_prompt
from packages.rag_core.src.vectorstore.chroma_store import get_module_chunks


def answer_question(question: str, module: str | None = None, difficulty: str | None = None, top_k: int = 4) -> dict:
    where_filter = build_where_filter(module=module, difficulty=difficulty)
    docs = retrieve_documents(question=question, top_k=top_k, where_filter=where_filter)

    if not docs:
        return build_answer_response(
            answer="No encontré información suficiente en los documentos para responder a esta pregunta.",
            docs=[],
        )

    prompt = build_answer_prompt(question=question, docs=docs)
    llm_answer = generate_answer(prompt)

    notebook_docs = get_notebook_chunks()
    related_labs = find_related_labs(docs, notebook_docs)

    response = build_answer_response(llm_answer, docs)
    response["related_labs"] = related_labs

    return response        
    
def study_question(question: str, level: str = "intermedio", module: str | None = None, difficulty: str | None = None, top_k: int = 4) -> dict:
    where_filter = build_where_filter(module=module, difficulty=difficulty)
    docs = retrieve_documents(question=question, top_k=top_k, where_filter=where_filter)

    if not docs:
        return build_answer_response(
            answer="No encontré información suficiente en los documentos para armar una tutoría.",
            docs=[],
        )

    # 1. Armamos el "cerebro" (System Prompt) con los documentos RAG y el nivel elegido
    study_sys_prompt = build_study_prompt(docs=docs, level=difficulty)

    # 2. El usuario solo hace la pregunta
    user_prompt = f"Profesor, tengo esta duda: '{question}'. Explícamelo a mi nivel y déjame preguntas de repaso."

    # 3. Disparamos la generación con nuestra dupla mágica
    llm_answer = generate_answer(prompt=user_prompt, system_prompt=study_sys_prompt)


    # 4. Magia de siempre: Vínculo cruzado entre PDFs y Notebooks
    notebook_docs = get_notebook_chunks()
    related_labs = find_related_labs(docs, notebook_docs)

    response = build_answer_response(llm_answer, docs)
    response["related_labs"] = related_labs

    return response

def quiz_question(question: str, level: str = "intermedio", module: str | None = None, difficulty: str | None = None, top_k: int = 4) -> dict:
    where_filter = build_where_filter(module=module, difficulty=difficulty)
    docs = retrieve_documents(question=question, top_k=top_k, where_filter=where_filter)

    if not docs:
        return build_answer_response("No hay suficiente contexto para armar un quiz de esto.", [])

    quiz_sys_prompt = build_quiz_prompt(docs=docs, level=level)
    user_prompt = f"Profesor, hazme un quiz de 3 preguntas de alternativas sobre: '{question}'."
    
    llm_answer = generate_answer(prompt=user_prompt, system_prompt=quiz_sys_prompt)

    notebook_docs = get_notebook_chunks()
    related_labs = find_related_labs(docs, notebook_docs)

    response = build_answer_response(llm_answer, docs)
    response["related_labs"] = related_labs

    return response

def summary_module(module: str) -> dict:
    docs = get_module_chunks(module)
    if not docs:
        return build_answer_response(f"No hay suficiente contexto para armar un resumen del módulo: '{module}'.", [])  
    
    summary_sys_prompt = build_summary_prompt(docs=docs, module=module)
    user_prompt = f"Genera el súper resumen de todo este contenido del módulo."
    
    llm_answer = generate_answer(prompt=user_prompt, system_prompt=summary_sys_prompt)
    
    # Aquí podríamos no mostrar citations (ya que es toda la clase) pero mantendremos 
    # la estandarización retornando un dict compatible
    return build_answer_response(llm_answer, docs[:5]) # Solo adjuntamos 5 docs referenciales
    