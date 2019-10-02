from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='attd-overview'),
    path('apply-leave/', views.apply_leave_req, name='attd-employee-leave-request'),
    path('manage-attendances/', views.manage_attendances, name='attd-manage-attendance'),
    path('approve-leave/', views.approve_leave, name='attd-approve-leave'),
]