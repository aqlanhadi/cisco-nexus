# Generated by Django 2.2.5 on 2019-10-22 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_guard_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='manager',
        ),
    ]
