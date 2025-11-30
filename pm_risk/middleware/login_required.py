from django.shortcuts import redirect
from django.urls import resolve
from django.conf import settings

EXEMPT_URL_NAMES = {
    'login',
    'logout',
    'admin:login',
    'admin:logout',
    'password_reset',
}

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            url_name = resolve(request.path_info).url_name
            if url_name not in EXEMPT_URL_NAMES:
                return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)