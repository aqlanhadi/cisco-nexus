from django import forms
from django.db import models
from users import models as user_models
from attendance_module.forms import LeaveDateTime
from django.contrib.auth.models import User

# Create your models here.

# class Leave(models.Model):
#     leaveid = models.AutoField(primary_key= True)
#     name = models.ForeignKey(User, on_delete=models.CASCADE)
#     startdate = models.DateField()
#     enddate = models.DateField()
#     starttime = models.DateTimeField()
#     endtime = models.DateTimeField()
#     supDoc = models.FileField(upload_to='support_docs')
#     reason = models.CharField(max_length=100)
#     status = models.BooleanField(default= False)

'''
user.entry.all() -> all records?
user.entry.filter(date='...') ->
'''

#Attendance Entries
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True, unique=True)
    hours_worked = models.DecimalField(default=10, max_digits=4, decimal_places=2)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['date',]

    def __str__(self):
        return '%s hours worked on %s' % (self.hours_worked, self.date)