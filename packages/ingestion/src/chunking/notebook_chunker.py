
def chunk_notebook(cells: list[dict], file_path: str) -> list[dict]:
    chunks = []
    
    for cell in cells:
        if cell["cell_type"] == "markdown":
            chunks.append({
                "id": f"{file_path}:md:{cell['cell_index']}",
                "source_file": file_path,
                "content": cell["content"],
                "type": "explanation"
            })
        
        elif cell["cell_type"] == "code":
            chunks.append({
                "id": f"{file_path}:code:{cell['cell_index']}",
                "source_file": file_path,
                "content": cell["content"],
                "type": "code"
            })
    
    return chunks