# Generated by Django 2.2.5 on 2019-10-22 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guard',
            name='manager',
        ),
    ]
