from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='attd-dash'),
    path('apply-leave/', views.leave_request, name='attd-leave-request'),
    path('review-leave/', views.leave_review, name='attd-leave-review'),
    #path('register-attd/', views.register_attendance , name='attd-register-attd'),
    path('register-attd/', views.RegisterAttendance.as_view(template_name='attendance_module/register-attendance.html') , name='attd-register-attd'),
]
