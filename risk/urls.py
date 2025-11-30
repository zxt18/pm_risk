from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='risk_home'),
    path('daily_risk_data/', views.daily_risk_data, name='daily_risk_data'),
    path('copy_to_today/', views.copy_to_today, name='copy_to_today'),
    path('submit_risk_data/', views.submit_risk_data, name='submit_risk_data')
]