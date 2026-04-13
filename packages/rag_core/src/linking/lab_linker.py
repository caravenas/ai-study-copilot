def find_related_labs(docs: list[dict], all_docs: list[dict]) -> list[dict]:
    theory_topics = set()
    explicit_labs = set()

    # 1. Recopilar identificadores duros (del manifest) y temas suaves extractados
    for d in docs:
        for t in d.get("topics", []):
            theory_topics.add(t)
            
        # Si el manifiesto inyectó explícitamente un lab, lo guardamos
        rel_lab = d.get("related_lab")
        if rel_lab:
            explicit_labs.add(rel_lab)

    related = []
    seen_files = set() # Para evitar recomendar el mismo Jupyter varias veces

    # 2. MATCH EXPLÍCITO (Prioridad 1)
    for d in all_docs:
        if d.get("source_type") != "notebook":
            continue
            
        src_file = d.get("source_file")
        if src_file in explicit_labs and src_file not in seen_files:
            related.append({
                "source_file": src_file,
                "topics": d.get("topics", []),
                "preview": d["content"][:120],
                "match_type": "explicit"
            })
            seen_files.add(src_file)

    # 3. MATCH SEMÁNTICO POR TEXTO (Prioridad 2 - Fallback)
    for d in all_docs:
        if d.get("source_type") != "notebook":
            continue
            
        src_file = d.get("source_file")
        if src_file in seen_files:
            continue
            
        overlap = theory_topics.intersection(set(d.get("topics", [])))

        if overlap:
            related.append({
                "source_file": src_file,
                "topics": list(overlap),
                "preview": d["content"][:120],
                "match_type": "topic_overlap"
            })
            seen_files.add(src_file)

    # Retornamos los top 3 laboratorios únicos. 
    # Siempre estarán primero los explícitos y luego los rellenados por semántica.
    return related[:3]
