from django.db import models
from attendance_module.models import Guard
from datetime import datetime

# Create your models here.
class Salary(models.Model):
    time = datetime.now()
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Guard, on_delete=models.CASCADE)
    pay_date = models.DateField(default=time)
    month = models.IntegerField(max_length=2, editable=False, blank=True, null=True)
    base_pay = models.FloatField(max_length=32, default=0)
    bonus = models.FloatField(max_length=32, default=0)

    class Meta:
        verbose_name_plural = "Salaries"

    def save(self, *args, **kwargs):
        month = int(self.pay_date.strftime('%m'))
        super(Salary, self).save(*args, **kwargs)