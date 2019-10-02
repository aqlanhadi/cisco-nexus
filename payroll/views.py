from django.shortcuts import render

# Create your views here.
def overview(request):
    return render(request, 'payroll/overview.html')

def salary(request):
    return render(request, 'payroll/man-salary-dash.html')

def payroll(request):
    return render(request, 'payroll/emp-payroll-dash.html')
# urlpatterns = [
#     path('', views.overview, name='pay-overview'),
#     path('salary/', views.salary, name='pay-salary'),
#     path('payrolls/', views.payrolls, name='pay-payroll'),
# ]