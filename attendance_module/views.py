from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .forms import LeaveDateTime, UploadFileForm
from users.decorators import group_required, is_guard
# Create your views here.

#employee
@is_guard
def leave_request(request):
    form = LeaveDateTime()
    return render(request, 'attendance_module/leave-request.html', {'form': form})

def upload_file(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['supDoc']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'attendance_module/leave-request.html', context)

def leave_list(request):
    return

#manager perm
@group_required('manager')
def leave_review(request):
    return render(request, 'attendance_module/leave-review.html')
#manager perm
@group_required('manager')
def register_attendance(request):
    return render(request, 'attendance_module/register-attendance.html')