from django import forms
from django.db import models
from users import models as user_models
from attendance_module.forms import LeaveDateTime
from django.contrib.auth.models import User

from datetime import datetime

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
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(default=datetime.now())
    end_datetime = models.DateTimeField(default=datetime.now())

    def hours_worked(self):
        #return '%s on %s' % self.user.username, self.start_datetime
        return (self.end_datetime - self.start_datetime).total_seconds() / 60 / 60

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['start_datetime',]

    def __str__(self):
        return '%s | %s hours worked on %s' % (self.user.username, str(self.hours_worked()), self.start_datetime)