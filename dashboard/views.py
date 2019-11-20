from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import decorator_user

# Create your views here.
@login_required
def dashboard(request):
    is_man = True if request.user.groups.filter(name='Managers').exists() else False
    is_guard = True if request.user.groups.filter(name='Guards').exists() else False
    context = {
        'is_man': is_man,
        'is_guard': is_guard
    }
    return render(request, 'dashboard/dashboard.html', context)