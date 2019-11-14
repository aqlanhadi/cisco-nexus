import json
import datetime
import pytz
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

from datatableview.views import Datatable, DatatableView
from django.contrib.auth.models import User
from .forms import LeaveDateTime, UploadFileForm
from .tables import GuardList
from .models import Entry, Guard
from .serializers import ShiftSerializer
from users.decorators import group_required, is_guard, is_manager

from calendar import HTMLCalendar, monthrange
# Create your views here.

PAY_PER_MIN = 0.06

current_guard = 0

tz = pytz.timezone('Asia/Kuala_Lumpur')
timezone.activate(tz)

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
#################CALENDAR VIEW################
# Author: Aqlan Nor Azman
def get_shift(request):
    g_id = request.GET['p_id']
    guard = User.objects.get(id=g_id)
    name = guard.first_name + " " + guard.last_name
    location = guard.guard.get().location.name
    pic_url = guard.profile.image.url

    u_entries = Entry.objects.filter(user__user__id=g_id, status='U')
    v_entries = Entry.objects.filter(user__user__id=g_id, status='V')

    u_mins = u_entries.aggregate(Sum('minutes_worked'))
    v_mins = v_entries.aggregate(Sum('minutes_worked'))
    print(u_mins)

    u_mws = u_mins['minutes_worked__sum']
    v_mws = v_mins['minutes_worked__sum']

    u_pay = int(u_mws) * PAY_PER_MIN if u_mws is not None else 0
    v_pay = int(v_mws) * PAY_PER_MIN if v_mws is not None else 0

    sum_pay = round(u_pay, 2) + round(v_pay, 2)

    u_entries_json = ShiftSerializer(u_entries, many=True, context={'color': 'white'})
    v_entries_json = ShiftSerializer(v_entries, many=True, context={'color': '#00FF99'})

    response = {
        'g_id': g_id,
        'name': name,
        'location': location,
        'pic_url': pic_url, 
        'u_data': u_entries_json.data, 
        'v_data': v_entries_json.data,
        'u_pay': str(round(u_pay, 2)),
        'v_pay': str(round(v_pay, 2)),
        'sum_pay' : str(round(sum_pay, 2)),
    }
    
    return JsonResponse(response)

def get_details(request):
    date = request.GET['date']
    guard_id = request.GET['g_id']
    shift = Entry.objects.get(user__user__id=guard_id, start_datetime=date)
    status = shift.status
    start = shift.start_datetime.astimezone(tz).strftime("%H:%M")
    end = shift.end_datetime.astimezone(tz).strftime("%H:%M")
    duration = str(datetime.timedelta(minutes=shift.minutes_worked))[:-3]

    hours = int(duration[:-3])
    d_col = 'red' if hours <= 11 else 'green'

    print(start)
    print(end)
    print(duration)
    response = {
        'g_id': guard_id,
        'status': status,
        'start': start,
        'end': end,
        'duration': duration,
        'd_col': d_col
    }

    return JsonResponse(response)

def verify_shift(request):
    date = request.GET['date']
    guard_id = request.GET['g_id']
    shift = Entry.objects.get(user__user__id=guard_id, start_datetime=date)
    
    if (shift.status == 'V'):
        shift.status = 'U'
    else:
        shift.status = 'V'

    shift.save()

    response = {
        'success': 'success',
        'status': shift.status,
    }

    return JsonResponse(response)

class GuardDatatable(Datatable):
    class Meta:
        columns = ['id','first_name']

class RegisterAttendance(DatatableView):
    model = User
    datatable_class = GuardDatatable

    g_id = None

    def post(self, request):
        response = {}
        if request.is_ajax():

            if 'shift_click' in request.POST:
                print(request.POST['shift_clicked'])
                response = {
                    'r_data': 'success'
                }
            
        return JsonResponse(response)


    def get_queryset(self):
        return User.objects.filter(guard__location__manager__username=self.request.user.username)
        