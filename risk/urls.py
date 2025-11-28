from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='risk_home'),
    path('daily_risk_data/', views.daily_risk_data, name='daily_risk_data')
]

