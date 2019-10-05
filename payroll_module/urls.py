from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='salary-dashboard'),
    path('breakdown/', views.breakdown, name='salary-breakdown'),
    path('history/', views.history, name='salary-history'),
]