def split_text(text: str, chunk_size: int = 800, overlap: int = 120) -> list[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = end - overlap

    return chunks


def chunk_pdf_document(pages: list[dict], file_path: str) -> list[dict]:
    chunks = []

    for page in pages:
        page_number = page["page"]
        page_text = page["text"]

        for idx, chunk_text in enumerate(split_text(page_text), start=1):
            chunks.append({
                "id": f"{file_path}:p{page_number}:c{idx}",
                "source_file": file_path,
                "page": page_number,
                "content": chunk_text,
            })

    return chunks