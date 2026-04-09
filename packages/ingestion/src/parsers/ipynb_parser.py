import json

def parse_notebook(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    cell_data = []
    
    for idx, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] not in ["markdown", "code"]:
            continue
        content = "".join(cell["source"]).strip()
        
        if not content:
            continue
            
        cell_data.append({
            "cell_index": idx,
            "cell_type": cell["cell_type"],
            "content": content
        })
    
    return cell_data
    
    