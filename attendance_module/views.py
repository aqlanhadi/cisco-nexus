import json
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
        response = {}
        if request.is_ajax():
            if 'p_id' in request.POST:
                print('[POST] received id -> ' + request.POST['p_id'])
                self.g_id = request.POST['p_id']
                print('current selection is id -> ' + self.g_id)
                guard = User.objects.get(id=self.g_id)
                text = guard.username
                unverified_entries = Entry.objects.filter(user__user__id=self.g_id, status='U')
                verified_entries = Entry.objects.filter(user__user__id=self.g_id, status='V')

                unverified_minutes = unverified_entries.aggregate(Sum('minutes_worked'))
                verified_minutes = verified_entries.aggregate(Sum('minutes_worked'))
                #unverified_shifts_json = serializers.serialize('json', unverified_shifts, fields=('start_datetime', 'end_datetime'))
                unverified_entries_json = ShiftSerializer(unverified_entries, many=True, context={'color': 'white'})
                verified_entries_json = ShiftSerializer(verified_entries, many=True, context={'color': '#00FF99'})
                # pays 6 cents a minute
                print("verified mins -> " + str(verified_minutes['minutes_worked__sum']) + " = " + str(verified_minutes['minutes_worked__sum']*.06))
                print("unverified -> " + str(unverified_minutes['minutes_worked__sum']) + " = " + str(unverified_minutes['minutes_worked__sum']*.06))
                print("total per month (verified+unverified) -> " + str((verified_minutes['minutes_worked__sum']*.06) + (unverified_minutes['minutes_worked__sum']*.06)))

                response = {
                    'text': text, 
                    'u_data': unverified_entries_json.data, 
                    'v_data': verified_entries_json.data,
                    'u_pay': str(unverified_minutes['minutes_worked__sum']*.06),
                    'v_pay': str(verified_minutes['minutes_worked__sum']*.06),
                    'sum_pay' : str((verified_minutes['minutes_worked__sum']*.06) + (unverified_minutes['minutes_worked__sum']*.06))
                }

            if 'shift_click' in request.POST:
                print(request.POST['shift_clicked'])
                response = {
                    'r_data': 'success'
                }
            
        return JsonResponse(response)


    def get_queryset(self):
        return User.objects.filter(guard__location__manager__username=self.request.user.username)
        