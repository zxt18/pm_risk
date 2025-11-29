from django.shortcuts import render
from django.http import JsonResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
import datetime
# from django.contrib.auth.decorators import login_required
from .models import DailyRisk
def index(request):
    today = datetime.date.today().isoformat()
    return render(request, "risk/pm_risk_table.html", {'today': today})

def daily_risk_data(request):
    date_str = request.GET.get('date')
    if date_str :
        selected_date = parse_date(date_str)    
    
        qs = DailyRisk.objects.filter(date = selected_date ).values(
            'book','risk','target','stop','worst_case_bp','worst_case_k','comment'
        ).order_by('-date')
        return JsonResponse(list(qs), safe=False)
    else : 
        qs = DailyRisk.objects.filter(date= datetime.date.today()).values(
            'book','risk','target','stop','worst_case_bp','worst_case_k','comment'
        )
        return JsonResponse(list(qs), safe=False)
    

def copy_to_today(request):
    today = timezone.localdate()  # Respects settings.TIME_ZONE
    yesterday = today - datetime.timedelta(days=1)
    
    qs = DailyRisk.objects.filter(date=yesterday).values(
        'book', 'risk', 'target', 'stop', 'worst_case_bp', 'worst_case_k', 'comment'
    )
    data = list(qs)
    return JsonResponse({
        'date': today.isoformat(),  # e.g., "2025-11-29"
        'entries': data
    })