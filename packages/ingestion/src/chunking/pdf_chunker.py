import re

def split_semantically(text: str, max_chunk_size: int = 800) -> list[str]:
    """
    Divide el texto respetando su flujo semántico (párrafos y oraciones), 
    evitando cortar ideas importantes por la mitad a lo bruto.
    """
    # 1. Separar suavemente por párrafos dobles
    paragraphs = re.split(r'\n\s*\n', text)
    
    chunks = []
    current_chunk = ""
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
            
        if len(current_chunk) + len(p) + 2 <= max_chunk_size:
            current_chunk += ("\n\n" + p) if current_chunk else p
        else:
            if current_chunk:
                chunks.append(current_chunk)
            
            # 2. Hard fallback: Si hay un párrafo enorme, lo partimos por oraciones
            if len(p) > max_chunk_size:
                sentences = re.split(r'(?<=\.)\s+', p)
                sub_chunk = ""
                for s in sentences:
                    if len(sub_chunk) + len(s) + 1 <= max_chunk_size:
                        sub_chunk += (" " + s) if sub_chunk else s
                    else:
                        if sub_chunk:
                            chunks.append(sub_chunk)
                        sub_chunk = s
                if sub_chunk:
                    current_chunk = sub_chunk
            else:
                current_chunk = p
                
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def chunk_pdf_document(pages: list[dict], file_path: str) -> list[dict]:
    chunks = []

    for page in pages:
        page_number = page["page"]
        page_text = page["text"]

        # Usamos nuestra nueva división semántica
        for idx, chunk_text in enumerate(split_semantically(page_text), start=1):
            chunks.append({
                "id": f"{file_path}:p{page_number}:c{idx}",
                "source_file": file_path,
                "page": page_number,
                "content": chunk_text,
            })

    return chunks
