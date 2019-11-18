from django.contrib import admin
from .models import *
from payroll_module.models import Salary

admin.site.site_title = 'Nexus Administration'

class EntryInline(admin.TabularInline):
    model = Entry

class ShiftStatusInlines(admin.TabularInline):
    model = ShiftStatus

class SalaryInlines(admin.TabularInline):
    model = Salary

class GuardAdmin(admin.ModelAdmin):
    inlines = [SalaryInlines, EntryInline, ShiftStatusInlines]

class ShiftInline(admin.TabularInline):
    model = Shift

class LocationAdmin(admin.ModelAdmin):
    inlines = [ShiftInline,]

# Register your models here.
admin.site.register(Location, LocationAdmin)
admin.site.register(Guard, GuardAdmin)
admin.site.register(Leave)