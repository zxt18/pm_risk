from django.shortcuts import render
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
# from django.contrib.auth.decorators import login_required
from .models import Book, DailyRisk
def index(request):
    today = datetime.date.today().isoformat()
    pm_users = User.objects.distinct().order_by('username')
    return render(request, "risk/pm_risk_table.html", {'today': today, 'pm_users': pm_users})

def _daily_risk_data(pm_identifier, selected_date):
    if not selected_date : 
        selected_date = timezone.localdate()  #by default selects latest day
            
    if pm_identifier :      
        user = User.objects.get(id=pm_identifier)

        books = Book.objects.filter(
            created_at__lte=selected_date,
            is_active=True,
            pm=user
        )

    # Fetch existing DailyRisk entries for this date and these books
        existing_risks = {
            dr.book_id: dr
            for dr in DailyRisk.objects.filter(
                book__in=books,
                date=selected_date
            )
        }

        # Build response with sensible defaults
        result = []
        for book in books:
            risk_obj = existing_risks.get(book.id)
            if risk_obj : 
                result.append({
                    'book_id': book.id,
                    'book_name': book.name,
                    'risk': float(risk_obj.risk) if risk_obj.risk is not None else 0.0,
                    'target': float(risk_obj.target) if risk_obj.target is not None else None,
                    'stop': float(risk_obj.stop) if risk_obj.stop is not None else None,
                    'worst_case_bp': float(risk_obj.worst_case_bp) if risk_obj.worst_case_bp is not None else 0.0,
                    'worst_case_k': float(risk_obj.worst_case_k) if risk_obj.worst_case_k is not None else 0.0,
                    'comment': risk_obj.comment if risk_obj else "",
                    'has_data': risk_obj is not None,
                })
                print(result)
        return result
    return None
        


def daily_risk_data(request):
    pm_identifier = request.GET.get('pm_id')
    date_str = request.GET.get('date') 
    selected_date = parse_date(date_str)
    result = _daily_risk_data(pm_identifier,selected_date)
    return JsonResponse(result, safe=False)
    

def copy_to_today(request):
    today = timezone.localdate()  # Respects settings.TIME_ZONE
    yesterday = today - datetime.timedelta(days=1)
    pm_identifier = request.GET.get('pm_id')
    result = _daily_risk_data(pm_identifier, yesterday) 
    return JsonResponse({
        'date': today.isoformat(),  # e.g., "2025-11-29"
        'entries': result
    })