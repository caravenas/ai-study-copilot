#def build_answer_response(question: str, llm_answer: str, docs: list[dict]) -> dict:
def build_answer_response(answer: str, docs: list[dict]) -> dict:
    citations = []
    unique_sources = set()
    related_labs = []

    for d in docs:
        source_key = f"{d['source_file']}:{d.get('page', 'unknown')}"
        
        if source_key not in unique_sources:
            citations.append({
                "source_file": d["source_file"],
                "page": d.get("page"),
                "chunk_id": d.get("chunk_id", "unknown"),
                "excerpt": d["content"][:180]
            })
            unique_sources.add(source_key)
    
    confidence = min(0.9, 0.5 + len(docs) * 0.15)

    return {
        "answer": answer,
        "citations": citations,
        "confidence": confidence
    }