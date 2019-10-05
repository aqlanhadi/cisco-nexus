from django.shortcuts import render
from .forms import LeaveDateTime
# Create your views here.

#employee
def leave_request(request):
    form = LeaveDateTime()
    return render(request, 'attendance_module/leave-request.html', {'form': form})

#manager perm
def leave_review(request):
    return render(request, 'attendance_module/leave-review.html')

#manager perm
def register_attendance(request):
    return render(request, 'attendance_module/register-attendance.html')