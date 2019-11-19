from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='salary-dashboard'),
    path('breakdown/', views.SalaryBreakdown.as_view(template_name='payroll_module/salary-breakdown.html'), name='salary-breakdown'),
    path('breakdown/get-salary', views.get_salary, name='get-salary'),
    path('charts', views.LineChartJSONView.as_view(), name='chart'),
    path('all/', views.EmployeeListView.as_view(), name='salary-list')
]