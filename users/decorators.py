from django.utils import six
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.http import HttpResponseForbidden, HttpResponseRedirect

def group_required(group, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(group, six.string_types):
            groups = (group, )
        else:
            groups = group
        # First check if the user has the permission (even anon users)

        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise HttpResponseForbidden()
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)



def is_guard(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='Guards').exists():
            return function(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return wrap

# def is_authorized(function):
#   @wraps(function)
#   def wrap(request, *args, **kwargs):

#         profile = request.user.get_profile()
#         if profile.usertype == 'Author':
#              return function(request, *args, **kwargs)
#         else:
#             return HttpResponseRedirect('/')

#   return wra