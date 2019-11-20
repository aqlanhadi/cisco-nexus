from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from attendance_module.models import Guard
from datatableview.views import Datatable, DatatableView
from .models import Salary
from .tables import SalaryList
from users.decorators import is_guard, is_manager, decorator_user

from random import randint, shuffle
from chartjs.colors import next_color, COLORS
from chartjs.views.lines import BaseLineChartView
from chartjs.util import date_range, value_or_null

# Create your views here.
@decorator_user(is_manager)
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

@is_guard
def dashboard(request):
    return render(request, 'payroll_module/salary-dashboard.html')

@is_guard
def breakdown(request):
    return render(request, 'payroll_module/salary-breakdown.html')

@is_guard
def get_salary(request):
    id = request.GET['s_id']
    record = Salary.objects.get(id=id)
    month = datetime.strftime(datetime.strptime(str(record.month), '%m'), '%B')
    paid = record.pay_date
    total = record.base_pay
    response = {
        'success':'success',
        'month': month,
        'total': total
    }
    return JsonResponse(response)

class SalaryDatatable(Datatable):
    class Meta:
        columns = ['id', 'pay_date', 'base_pay']

@decorator_user(is_guard)
class SalaryBreakdown(DatatableView):
    model = Salary
    datatable_class = SalaryDatatable
    def get_queryset(self):
        return Salary.objects.filter(user__user__username=self.request.user.username)

@is_guard
def history(request):
    return render(request, 'payroll_module/salary-history.html')

####CHART TEST####
class ChartMixin(object):
    def get_providers(self):
        """Return names of datasets."""
        return ["Central", "Eastside", "Westside"]

    def get_labels(self):
        """Return 7 labels."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_data(self):
        """Return 3 random dataset to plot."""
        def data():
            """Return 7 randint between 0 and 100."""
            return [randint(0, 100) for x in range(7)]

        return [data() for x in range(3)]
    
    def get_colors(self):
        """Return a new shuffle list of color so we change the color
        each time."""
        colors = COLORS[:]
        shuffle(colors)
        return next_color(colors)

class LineChartJSONView(ChartMixin, BaseLineChartView):
    pass
