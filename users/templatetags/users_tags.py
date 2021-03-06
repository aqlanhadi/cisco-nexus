from django import template

register = template.Library()

@register.filter
def is_manager(user):
    if user.is_superuser:
        return True
    else:
        return user.groups.filter(name='Managers').exists()

@register.filter
def is_guard(user):
    if user.is_superuser:
        return True
    else:
        return user.groups.filter(name='Guards').exists()

@register.filter(name='is_in')
def is_in(user, group):
    return user.groups.filter(name=group).exists() 