# Generated by Django 2.2.5 on 2019-11-16 10:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_module', '0029_auto_20191116_1834'),
    ]

    operations = [
        migrations.RenameField(
            model_name='leave',
            old_name='suport_docs',
            new_name='support_docs',
        ),
        migrations.AlterField(
            model_name='entry',
            name='end_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 18, 56, 6, 876027)),
        ),
        migrations.AlterField(
            model_name='entry',
            name='start_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 11, 16, 18, 56, 6, 875995)),
        ),
    ]