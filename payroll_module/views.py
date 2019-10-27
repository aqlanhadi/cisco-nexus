from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import ListView
from django.core import serializers
from .serializers import GuardSerializer
from users.models import Guard
from rest_framework.renderers import JSONRenderer
import json

# Create your views here.

class EmployeeListView(ListView):
    model = Guard
    template_name = 'payroll_module/salary-list.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        guards = User.objects.filter(guard__location__manager__username=user)
        serializer_class = GuardSerializer(guards, many=True)
        serialized_data =  json.dumps(serializer_class.data)
        print(serialized_data)
        print("[GET]")
        return render(request, self.template_name, {'guards':serialized_data})

    def post(self, request, *args, **kwargs):
        print("[POST]")
        return render(request, self.template_name)

def dashboard(request):
    return render(request, 'payroll_module/salary-dashboard.html')

def breakdown(request):
    return render(request, 'payroll_module/salary-breakdown.html')

def history(request):
    return render(request, 'payroll_module/salary-history.html')