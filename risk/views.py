import datetime
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User
from django.utils import timezone

from .services import fetch_risk_data, save_risk_data


def index(request):
    return render(request, "risk/pm_risk_table.html", {
        "today": datetime.date.today().isoformat(),
        "pm_users": User.objects.order_by("username"),
    })


def daily_risk_data(request):
    pm_id = request.GET.get("pm_id")

    date = parse_date(request.GET.get("date")) or timezone.localdate()
    result = fetch_risk_data(pm_id, date)
    return JsonResponse(result, safe=False)


def copy_to_today(request):
    pm_id = request.GET.get("pm_id")
    today = timezone.localdate()
    yesterday = today - datetime.timedelta(days=1)
    entries = fetch_risk_data(pm_id, yesterday)
    return JsonResponse({
        "date": today.isoformat(),
        "entries": entries
    })


@require_POST
@csrf_exempt
def submit_risk_data(request):
    try:
        body = json.loads(request.body)
        pm_id = body.get("pm_id")
        date = parse_date(body.get("date"))
        entries = body.get("entries", [])

        if not pm_id or not date:
            return JsonResponse({"error": "pm_id and date required"}, status=400)

        pm = User.objects.get(id=pm_id)
        save_risk_data(pm, date, entries)

        return JsonResponse({"message": "Saved successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)