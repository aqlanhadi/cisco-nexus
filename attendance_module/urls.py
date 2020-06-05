from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='attd-dash'),
    path('apply-leave/', views.new_leave_request, name='attd-leave-request'),
    path('review-leave/', views.LeaveReview.as_view(template_name='attendance_module/leave-review.html'), name='attd-leave-review'),
    path('review-leave/details/', views.get_leave_details, name='get-leave-details'),
    path('review-leave/approve', views.approve, name='attd-approve'),
    path('review-leave/reject', views.reject, name='attd-reject'),
    #path('register-attd/', views.register_attendance , name='attd-register-attd'),
    path('register-attd/', views.RegisterAttendance.as_view(template_name='attendance_module/register-attendance.html') , name='attd-register-attd'),
    path('register-attd/get-shift/', views.get_shift, name='attd-get-shift'),
    path('register-attd/get-details/', views.get_details, name='attd-get-details'),
    path('register-attd/verify-shift/', views.verify_shift, name='attd-verify'),
    path('resgister-attd/save-salary/', views.save_salary, name='attd-submit')
]
