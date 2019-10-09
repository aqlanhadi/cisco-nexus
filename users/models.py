from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Guard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='manager', on_delete=models.CASCADE)

    user.is_guard = True

    def __str__(self):
        return "Guard ID: "

class Role(models.Model):
    GUARD = 1
    MANAGER = 2
    STAFF = 3
    CLIENT = 4
    ADMIN = 5
    ROLE_CHOICES = (
        (GUARD, 'guard'),
        (MANAGER, 'manager'),
        (STAFF, 'staff'),
        (CLIENT, 'client'),
        (ADMIN, 'admin'),
    )

    id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

    def __str__(self):
        return self._get_id_display()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

#Disallow self-refferential Foreign Key (managers)
class ManagerAdmin(admin.ModelAdmin):
    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.object_id = object_id
        return super(ManagerAdmin, self).change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'manager':
            kwargs['queryset'] = User.objects.exclude(pk=self.object_id)
        return super(ManagerAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)