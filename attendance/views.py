from django.shortcuts import render

# Create your views here.
def overview(request):
    return render(request, 'attendance/overview.html')

def apply_leave_req(request):
    return render(request, 'attendance/emp-leave-req.html')

def manage_attendances(request):
    return render(request, 'attendance/man-attendance.html')

def approve_leave(request):
    return render(request, 'attendance/man-leave-approve.html')



#     path('', views.overview, name='attd-overview'),
#     path('apply-leave/', views.employee_leave_req, name='attd-employee-leave-request'),
#     path('manage-attendances/', views.manage_attendances, name='attd-manage-attendance'),
#     path('approve-leave/', views.approve_leave, name='attd-approve-leave'),
