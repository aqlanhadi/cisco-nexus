from django.shortcuts import render

# Create your views here.

#employee
def leave_request(request):
    return render(request, 'attendance_module/leave-request.html')

#manager perm
def leave_review(request):
    return render(request, 'attendance_module/leave-review.html')

#manager perm
def register_attendance(request):
    return render(request, 'attendance_module/register-attendance.html')