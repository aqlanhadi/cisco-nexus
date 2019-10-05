from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'payroll_module/salary-dashboard.html')

def breakdown(request):
    return render(request, 'payroll_module/salary-breakdown.html')

def history(request):
    return render(request, 'payroll_module/salary-history.html')