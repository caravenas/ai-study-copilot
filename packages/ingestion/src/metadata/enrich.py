from packages.ingestion.src.metadata.topic_extractor import extract_topics

def enrich_chunks(chunks: list[dict], extra_metadata: dict) -> list[dict]:
    enriched = []
    
    for chunk in chunks:
        topics = extract_topics(chunk["content"])
        
        item = {
            **chunk,
            **extra_metadata,
            "topics": topics
        }
        
        enriched.append(item)
    
    return enriched