import json
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.core.files.storage import FileSystemStorage

from datatableview.views import Datatable, DatatableView
from django.contrib.auth.models import User
from users.models import Guard
from .forms import LeaveDateTime, UploadFileForm
from .tables import GuardList
from .models import Entry
from .serializers import ShiftSerializer
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
#################CALENDAR VIEW################
# Author: Aqlan Nor Azman
class GuardDatatable(Datatable):
    class Meta:
        columns = ['id','username']

class RegisterAttendance(DatatableView):
    model = User
    datatable_class = GuardDatatable

    g_id = None

    def post(self, request):
        if request.is_ajax():
            if 'p_id' in request.POST:
                print('[POST] received id -> ' + request.POST['p_id'])
                self.g_id = request.POST['p_id']
                print('current selection is id -> ' + self.g_id)
                guard = User.objects.get(id=self.g_id)
                text = guard.username
                unverified_shifts = Entry.objects.filter(user__id=self.g_id)
                #unverified_shifts_json = serializers.serialize('json', unverified_shifts, fields=('start_datetime', 'end_datetime'))
                unverified_shifts_json = ShiftSerializer(unverified_shifts, many=True)
                print(unverified_shifts_json.data)
                return JsonResponse({'text': text, 'shift_data': unverified_shifts_json.data})

            if 'render_events' in request.POST:
                r_date = request.POST['render_events']
                #if User.objects.get(id=6).entry_set.get(date=str(r_date)) is not None:
                hours_worked = User.objects.get(id=request.POST['g_id']).entry_set.get(date="2019-11-02").hours_worked if request.POST['g_id'] == '6' else 0
                print("> hours_worked: " + str(hours_worked))
                return JsonResponse({'r_data': str(hours_worked)})
                #else:
                #    return JsonResponse({'r_data': 0})


    def get_queryset(self):
        return User.objects.filter(guard__location__manager__username=self.request.user.username)
        