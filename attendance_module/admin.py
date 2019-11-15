from django.contrib import admin
from .models import *

class EntryInline(admin.TabularInline):
    model = Entry

class ShiftStatusInlines(admin.TabularInline):
    model = ShiftStatus

class GuardAdmin(admin.ModelAdmin):
    inlines = [EntryInline, ShiftStatusInlines]

class ShiftInline(admin.TabularInline):
    model = Shift

class LocationAdmin(admin.ModelAdmin):
    inlines = [ShiftInline,]

# Register your models here.
admin.site.register(Location, LocationAdmin)
admin.site.register(Guard, GuardAdmin)