import json
import os
from pathlib import Path
from packages.ingestion.src.metadata.topic_extractor import extract_topics

# Usamos caché global básica para evitar leer el disco en cada chunk
MANIFEST_CACHE = None

def load_manifest() -> dict:
    global MANIFEST_CACHE
    if MANIFEST_CACHE is not None:
        return MANIFEST_CACHE

    # Construimos la ruta absoluta al archivo
    base_dir = Path(__file__).resolve().parents[4]
    manifest_path = base_dir / "data" / "manifest.json"

    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            MANIFEST_CACHE = json.load(f)
    else:
        MANIFEST_CACHE = {}
    
    return MANIFEST_CACHE
    

def enrich_chunks(chunks: list[dict], extra_metadata: dict) -> list[dict]:
    enriched = []
    
    # 1. Obtener la metadata del manifiesto cruzando por nombre de archivo
    manifest_data = load_manifest()
    source_file = extra_metadata.get("source_file", "")
    filename = os.path.basename(source_file)
    
    # Si el archivo está en manifest.json, sacamos sus campos (module, difficulty, week, etc.)
    file_curriculum = manifest_data.get(filename, {})

    for chunk in chunks:
        # 2. Extraer temas del contenido
        topics = extract_topics(chunk["content"])
        
        # 3. Construir el chunk final
        item = {
            **chunk,
            **extra_metadata,
            **file_curriculum,
            "topics": topics
        }
        
        enriched.append(item)
    
    return enriched