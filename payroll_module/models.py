from django.db import models
from attendance_module.models import Guard
from datetime import datetime

# Create your models here.
class Salary(models.Model):
    time = datetime.now()
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Guard, on_delete=models.CASCADE)
    pay_date = models.DateField(default=time)
    month = models.IntegerField(max_length=2, editable=False, default=int(time.strftime('%m')))
    base_pay = models.FloatField(max_length=32, default=0)
    bonus = models.FloatField(max_length=32, default=0)

    class Meta:
        verbose_name_plural = "Salaries"