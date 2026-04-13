
def chunk_notebook(cells: list[dict], file_path: str) -> list[dict]:
    chunks = []
    current_section = "setup" # Asumimos que los jupyters parten configurando el entorno

    for idx, cell in enumerate(cells):
        content = cell.get("content", "").strip()
        if not content:
            continue
        
        if cell["cell_type"] == "markdown":
            # Detección semántica simple basada en encabezados Markdown
            if content.startswith("# "):
                lower_content = content.lower()
                if "ejercicio" in lower_content or "exercise" in lower_content or "práctica" in lower_content:
                    current_section = "exercise"
                elif "conclusión" in lower_content or "analysis" in lower_content:
                    current_section = "analysis"
                else:
                    current_section = "theory"
            
            chunks.append({
                "id": f"{file_path}:md:{idx}",
                "source_file": file_path,
                "content": content,
                "type": "explanation",
                "section": current_section # Inyectamos este nuevo dato crítico
            })
            
        elif cell["cell_type"] == "code":
            lines = content.split('\n')
            
            # Filtro inteligente de ruido: ignoramos pip, imports simples y variables fantasma
            meaningful_lines = [
                l for l in lines 
                if l.strip() and not l.strip().startswith(("!", "%", "import ", "from "))
            ]
            
            # Si la gran mayoría de la celda es instalación o imports, la ignoramos completamente
            if not meaningful_lines:
                continue
                
            chunks.append({
                "id": f"{file_path}:code:{idx}",
                "source_file": file_path,
                "content": content,
                "type": "code",
                "section": current_section # Inyectamos este nuevo dato crítico
            })
    
    return chunks