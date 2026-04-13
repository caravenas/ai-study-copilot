def build_where_filter(
    module: str | None = None, 
    difficulty: str | None = None, 
    week: int | None = None, 
    course: str | None = None
) -> dict | None:
    conditions = []
    
    if module:
        conditions.append({"module": module})
    if difficulty:
        conditions.append({"difficulty": difficulty})
    if week:
        conditions.append({"week": week})
    if course:
        conditions.append({"course": course})
    
    if not conditions:
        return None

    if len(conditions) == 1:
        return conditions[0]
    
    # ChromaDB requiere la sintaxis "$and" para múltiples condiciones
    return {"$and": conditions}