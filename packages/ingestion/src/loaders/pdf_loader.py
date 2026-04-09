from typing import List
from pypdf import PdfReader

def load_pdf(file_path: str) -> List[dict]:
    reader = PdfReader(file_path)
    pages = []
    
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append({
                "page": idx,
                "text": text
            })
    return pages

    