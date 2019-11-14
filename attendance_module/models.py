from django import forms
from django.db import models
from attendance_module.forms import LeaveDateTime
from django.contrib.auth.models import User, Group

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

class Location(models.Model):
    name = models.CharField(max_length=50)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name':'Managers'}, null=True)

    def __str__(self):
        return self.name
    
    def guards(self):
        return Guard.objects.filter(location=self)

class Shift(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    shift_start = models.TimeField()
    shift_end = models.TimeField()

    def __str__(self):
        return '%s to %s shift at %s' % (self.shift_start, self.shift_end, self.location)

class Guard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guard')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    guard_group = Group.objects.get(name='Guards')
    guard_group.user_set.add()

    shift = models.ManyToManyField(Shift, through='ShiftStatus')

    def __str__(self):
        return self.user.username

class ShiftStatus(models.Model):
    STATUS_CHOICES = [('A', 'Active'),('I', 'Inactive')]
    guard = models.ForeignKey(Guard, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')

    class Meta:
        verbose_name = "Shift Status"
        verbose_name_plural = "Shift Statuses"

    def __str__(self):
        return '%s shift for %s is %s' % (self.shift.shift_start, self.guard.user.username, self.status)
    
#Attendance Entries
class Entry(models.Model):
    STATUS_CHOICES = [('U', 'Unverified'), ('V', 'Verified')]
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='U')
    user = models.ForeignKey(Guard, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField(default=datetime.now())
    end_datetime = models.DateTimeField(default=datetime.now())
    minutes_worked = models.IntegerField(max_length=32, editable=False, default=0)

    def save(self, *args, **kwargs):
        self.minutes_worked = (self.end_datetime - self.start_datetime).total_seconds() / 60
        super(Entry, self).save(*args, **kwargs)
    
    def verify(self):
        self.status = 'V'
    
    def unverify(self):
        self.status = 'U'

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ['start_datetime',]

    def __str__(self):
        return '%s | %s minutes worked on %s' % (self.user.user.username, str(self.minutes_worked), self.start_datetime)