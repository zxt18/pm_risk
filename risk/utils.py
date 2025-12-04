from risk.models import PMPermission, User


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

def user_can_edit_pm(user : User, pm):
    if user.can_edit_all_pms or user == pm: 
        return True
    return PMPermission.objects.filter(
        user=user,
        pm=pm,
        permission=PMPermission.EDIT
    ).exists()

def user_can_view_pm(user : User, pm):
    if user == pm or user.can_view_all_pms or user.can_edit_all_pms:
        return True
    return PMPermission.objects.filter(
        user=user,
        pm=pm,
        permission__in=[PMPermission.VIEW, PMPermission.EDIT]
    ).exists()
  
