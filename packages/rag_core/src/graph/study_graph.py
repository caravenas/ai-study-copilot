from langgraph.graph import StateGraph, START, END
from packages.rag_core.src.graph.state import StudyState
from packages.rag_core.src.graph.nodes import (
    classify_intent,
    retrieve_context,
    tutor_agent,
    coder_agent,
    quiz_agent,
    synthesize_response,
    grade_documents, # nuevo para Corrective RAG (CRAG)
    rewrite_query, # nuevo para Corrective RAG (CRAG)
    handle_no_context # nuevo para Corrective RAG (CRAG)
)

MAX_RETRIEVAL_ATTEMPTS = 2

def route_by_intent(state: StudyState) -> str:
    """Función de routing: decide qué agente usar según el intent."""
    return state["intent"]

def route_after_grading(state: StudyState) -> str:
    if state["docs_relevant"]:
        return state["intent"]
    if state.get("retrieval_attempts", 0) >= MAX_RETRIEVAL_ATTEMPTS:
        return "no_context"   # ← en vez de mandar al agente con docs malos
    return "rewrite"


def build_study_graph():
    """Contruye y compila el grafo de agentes"""
    graph = StateGraph(StudyState)

    # 1. Añadir nodos
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("tutor_agent", tutor_agent)
    graph.add_node("coder_agent", coder_agent)
    graph.add_node("quiz_agent", quiz_agent)
    graph.add_node("synthesize_response", synthesize_response)
    
    # 1.1 Nodos para CRAG
    graph.add_node("grade_documents", grade_documents)
    graph.add_node("rewrite_query", rewrite_query)
    graph.add_node("handle_no_context", handle_no_context)

    # 2. Definir flujo: START → classify → retrieve
    graph.add_edge(START, "classify_intent")
    graph.add_edge("classify_intent", "retrieve_context")
    graph.add_edge("retrieve_context", "grade_documents") # nuevo nodo para CRAG

    # 3. Routing condicional: retrieve → (tutor | coder | quizzer)
    graph.add_conditional_edges(
        "grade_documents",
        route_after_grading,
        {
            "teoria": "tutor_agent",
            "codigo": "coder_agent",
            "quiz": "quiz_agent",
            "rewrite": "rewrite_query",
            "no_context": "handle_no_context"  # ← nueva ruta
        }
    )

    # El rewrite_query regresa a retrieve_context para intentar con la nueva query
    graph.add_edge("rewrite_query", "retrieve_context")

    # 4. Todos los agentes convergen en synthesize → END
    graph.add_edge("tutor_agent", "synthesize_response")
    graph.add_edge("coder_agent", "synthesize_response")
    graph.add_edge("quiz_agent", "synthesize_response")
    graph.add_edge("synthesize_response", END)

    # 5. Compilar
    return graph.compile()

# Singleton: compilar una vez, reusar siempre
study_graph = build_study_graph()