from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView
from attendance_module.models import Guard
from .tables import SalaryList

# Create your views here.

class EmployeeListView(ListView):
    model = Guard
    template_name = 'payroll_module/salary-list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        guards = SalaryList(User.objects.filter(guard__location__manager__username=user))
        print("[GET]")
        return render(request, self.template_name, {'table':guards})

    def post(self, request, *args, **kwargs):
        print("[POST]")
        return render(request, self.template_name)

def dashboard(request):
    return render(request, 'payroll_module/salary-dashboard.html')

def breakdown(request):
    return render(request, 'payroll_module/salary-breakdown.html')

def history(request):
    return render(request, 'payroll_module/salary-history.html')