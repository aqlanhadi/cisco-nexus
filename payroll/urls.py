from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='pay-overview'),
    path('salary/', views.salary, name='pay-salary'),
    path('manage/', views.payroll, name='pay-payroll'),
]