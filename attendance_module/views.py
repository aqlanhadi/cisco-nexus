import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from users.models import Guard
from .forms import LeaveDateTime, UploadFileForm
from users.decorators import group_required, is_guard, is_manager

from calendar import HTMLCalendar, monthrange
# Create your views here.

def dashboard(request):
    return render(request, 'attendance_module/dashboard.html')

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

#manager perm
@is_manager
def leave_review(request):
    return render(request, 'attendance_module/leave-review.html')
#manager perm

@is_manager
def register_attendance(request):
    # once loaded -> gather all employee objects (the one u manage)
    #display first entry:
    #   populate calendar with colors? -> access each day entry css
    #   lock other months
    # iterate++ when next
    user = request.user
    # Gather all the guards that the user is managing
    guards = Guard.objects.filter(location__manager__username=user)

    if request.is_ajax():
        date_clicked = request.POST['date_clicked']
        entry_today = user.entry_set.get(date=date_clicked)
        if entry_today is not None:
            text = "requested for " + entry_today.date.strftime("%D-%M-%Y")
            hours_worked = entry_today.hours_worked
        else:
            text = "no record found"
        css = "day-highlight"
        return JsonResponse({'data': text, 'hours_worked':hours_worked, 'css':css})

    json_entry = "{ selectable:true }"
    json_data = json.dumps(json_entry)
    return render(request, 'attendance_module/register-attendance.html', {'user': user, 'guards':guards.iterator() ,'fc_json': json_entry })


#################CALENDAR VIEW################
# Author: Aqlan Nor Azman

