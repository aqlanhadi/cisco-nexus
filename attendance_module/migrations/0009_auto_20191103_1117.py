# Generated by Django 2.2.5 on 2019-11-03 11:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_module', '0008_auto_20191103_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='end_datetime',
            field=models.DateField(default=datetime.datetime(2019, 11, 3, 11, 17, 9, 198774)),
        ),
        migrations.AlterField(
            model_name='entry',
            name='start_datetime',
            field=models.DateField(default=datetime.datetime(2019, 11, 3, 11, 17, 9, 198745)),
        ),
    ]