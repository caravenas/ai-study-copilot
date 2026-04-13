from packages.rag_core.src.retrieval.retriever import retrieve_documents
from packages.rag_core.src.prompts.answer_prompt import build_answer_prompt
from packages.rag_core.src.synthesis.answer_builder import build_answer_response
from packages.rag_core.src.llm.client import generate_answer
from packages.rag_core.src.vectorstore.chroma_store import get_notebook_chunks

from packages.rag_core.src.linking.lab_linker import find_related_labs
from packages.rag_core.src.retrieval.filters import build_where_filter


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
        
    
    

