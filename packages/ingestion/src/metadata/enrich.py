def enrich_chunks(chunks: list[dict], extra_metadata: dict) -> list[dict]:
    enriched = []
    for chunks in chunks:
        item = {**chunks, **extra_metadata}
        enriched.append(item)
    return enriched