import json
from datetime import datetime, timedelta
import pytz
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

from datatableview import columns
from datatableview.views import Datatable, DatatableView
from django.contrib.auth.models import User
from .forms import LeaveForm
from .tables import GuardList
from .models import Leave, Entry, Guard
from .serializers import ShiftSerializer
from users.decorators import group_required, is_guard, is_manager
from payroll_module.models import Salary
from calendar import HTMLCalendar, monthrange
# Create your views here.

PAY_PER_MIN = 0.06

current_guard = 0

tz = pytz.timezone('Asia/Kuala_Lumpur')
timezone.activate(tz)

def upload(file):
    fs = FileSystemStorage()
    name = fs.save(file.name, file)
    uploaded_to = fs.url(name)
    print("file uploaded to " + uploaded_to)

def dashboard(request):
    return render(request, 'attendance_module/dashboard.html')

def new_leave_request(request):
    if request.method == "POST":
        user = request.user
        s_date = datetime.strptime(request.POST['start-date'], '%m/%d/%Y')
        s_time = datetime.strptime(request.POST['start-time'], '%I:%M %p').time()
        e_date = datetime.strptime(request.POST['end-date'], '%m/%d/%Y')
        e_time = datetime.strptime(request.POST['end-time'], '%I:%M %p').time()
        reason = request.POST['reason']
        file = request.FILES.get('file', False)
        #if file:
            #upload(request.FILES['file'])
        
        start_dt = datetime.combine(s_date, s_time)
        end_dt = datetime.combine(e_date, e_time)
        l = Leave(
            user=user.guard.get(), 
            start_datetime=start_dt, 
            end_datetime=end_dt, 
            support_docs=request.FILES['file'] if file else None, 
            reason=reason
        )
        l.save()
        print("s_ts-: " + start_dt.strftime("%d/%m/%Y %I:%M %p / %H:%M"))
        
        #l = Salary(user=user.guard.get())

    return render(request, 'attendance_module/leave-request.html') 

#manager perm
@is_manager
def leave_review(request):
    return render(request, 'attendance_module/leave-review.html')

def approve(request):
    id = request.GET['id']
    leave = Leave.objects.get(id=id)

    leave.status = 'A'
    leave.save()
    response = {
        'status': leave.status,
        'success':'success'
    }
    return JsonResponse(response)

def reject(request):
    id  = request.GET['id']
    leave = Leave.object.get(id=id)

class LeaveDatatable(Datatable):
    user = columns.CompoundColumn("Employee", sources=['user__user__first_name', 'user__user__last_name'])
    location = columns.TextColumn("Location", source=['user__location'])
    date = columns.DateColumn("Requested For", source=None, processor='get_date')
    class Meta:
        columns = [
            'user',
            'location',
            'date',
            'status'
        ]
    
    def get_date(self, instance, **kwargs):
        return datetime.strftime(instance.start_datetime, "%A, %d %B %Y")

class LeaveReview(DatatableView):
    model = Leave
    datatable_class = LeaveDatatable

    def get_queryset(self):
        return Leave.objects.filter(user__location__manager__username=self.request.user.username)

def get_leave_details(request):
    id = request.GET['leave_id']
    leave = Leave.objects.get(id=id)
    requestor = leave.user
    name = requestor.user.first_name + " " + requestor.user.last_name
    g_id = requestor.user.id
    img = requestor.user.profile.image.url
    location = requestor.location.name
    support_doc_url = leave.support_docs.url if not None else "NA"
    status = leave.status
    reason = leave.reason
    print(id)

    response = {
        'success':'success',
        'name': name,
        'id': g_id,
        'img': img,
        'location': location,
        'reason': reason,
        'doc_url': support_doc_url,
        'status': status
    }

    return JsonResponse(response)

#manager perm
#################CALENDAR VIEW################
# Author: Aqlan Nor Azman
def calculate_salary(mins):
    pay = int(mins) * PAY_PER_MIN if mins is not None else 0
    return round(pay, 2)

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
    duration = str(timedelta(minutes=shift.minutes_worked))[:-3]

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

def save_salary(request):
    guard_id = request.GET['g_id']
    guard = Guard.objects.get(user__id=guard_id)
    v_entries = Entry.objects.filter(user__user__id=guard_id, status='V')
    total_min = v_entries.aggregate(Sum('minutes_worked'))['minutes_worked__sum']

    total_sal = calculate_salary(total_min)
    entry = Salary(user=guard, base_pay=total_sal)
    entry.save()

    response = {
        'success':'success'
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
        