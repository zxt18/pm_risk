from django.shortcuts import render

def index(request):
    return render(request, "risk/pm_risk_table.html")
