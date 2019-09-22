from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def starter(request):
    return render(request, 'nexus/index.html')

def dashboard(request):
    #return HttpResponse("hi")
    return render(request, 'dashboard/dashboard.html', {'title':'Dashboard'})
