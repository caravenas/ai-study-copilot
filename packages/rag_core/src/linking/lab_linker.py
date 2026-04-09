def find_related_labs(docs: list[dict], all_docs: list[dict]) -> list[dict]:
    theory_topics = set()

    for d in docs:
        for t in d.get("topics", []):
            theory_topics.add(t)

    related = []

    for d in all_docs:
        if d.get("source_type") != "notebook":
            continue

        overlap = theory_topics.intersection(set(d.get("topics", [])))

        if overlap:
            related.append({
                "source_file": d["source_file"],
                "topics": list(overlap),
                "preview": d["content"][:120]
            })

    return related[:3]