from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def starter(request):
    return render(request, 'nexus/index.html')

@login_required
def dashboard(request):
    #return HttpResponse("hi")
    print(request.user)
    return render(request, 'dashboard/dashboard.html', {'title':'Dashboard'})

