def _serialize_risks(books, risks):
    """
    Helper to serialize books and their associated DailyRisk objects.
    """
    result = []
    for book in books:
        r = risks.get(book.id)
        result.append({
            "book_id": book.id,
            "book_name": book.name,
            "risk": getattr(r, "risk", None),
            "target": getattr(r, "target", None),
            "stop": getattr(r, "stop", None),
            "worst_case_bp": getattr(r, "worst_case_bp", None),
            "worst_case_k": getattr(r, "worst_case_k", None),
            "comment": getattr(r, "comment", None),
        })
    return result

