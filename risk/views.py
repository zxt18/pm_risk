import datetime
import json
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import User
from django.utils import timezone

from risk.utils import user_can_edit_pm, user_can_view_pm
from .services import fetch_risk_data, get_last_risk_data, save_risk_data


def index(request):
    return render(request, "risk/pm_risk_table.html", {
        "today": datetime.date.today().isoformat(),
        "pm_users": User.objects.order_by("username"),
    })


def daily_risk_data(request):
    pm_id = request.GET.get("pm_id")
    date = parse_date(request.GET.get("date")) or timezone.localdate()
    pm = User.objects.get(id=pm_id)
    if user_can_view_pm(request.user,pm): 
        result = fetch_risk_data(pm, date)
        return JsonResponse(result, safe=False)
    else : 
        return JsonResponse({"error": f"{request.user.username} does not have permissions to view {pm.username}'s books"}, status=500)


def copy_to_today(request):
    pm_id = request.GET.get("pm_id")
    today = timezone.localdate()
    pm = User.objects.get(id=pm_id)
    entries = get_last_risk_data(pm, today)
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
        if user_can_edit_pm(request.user,pm) : 
            if date < timezone.localdate():
                return JsonResponse({"error": "You can't edit the past"}, status=400)  

            save_risk_data(pm, date, entries)
            return JsonResponse({"message": "Saved successfully!"})
        else : 
            return JsonResponse({"error": f"{request.user} does not have permissions to edit {pm}'s books"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    


# LOGIN code
from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get("next") or settings.LOGIN_REDIRECT_URL
            return redirect(next_url)

    return render(request, "risk/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect(settings.LOGIN_URL)