from django import forms
from django.db import models
from attendance_module.forms import LeaveDateTime
from django.contrib.auth.models import User

# Create your models here.

class Leave(models.Model):
    leaveid = models.AutoField(primary_key= True)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    startdate = models.DateField()
    enddate = models.DateField()
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    supDoc = models.FileField(upload_to='support_docs')
    reason = models.CharField(max_length=100)
    status = models.BooleanField(default= False)

def __str__(self):
    return self.leaveid