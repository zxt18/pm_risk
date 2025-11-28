from django.shortcuts import render
from django.http import JsonResponse
from .models import DailyRisk


def index(request):
    return render(request, "risk/pm_risk_table.html")

def daily_risk_data(request):
    qs = DailyRisk.objects.all().values(
        'book','risk','target','stop','worst_case_bp','worst_case_k','comment'
    ).order_by('-date')
    return JsonResponse(list(qs), safe=False)