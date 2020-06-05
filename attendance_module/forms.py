#from bootstrap4_datetime.widgets import DateTimePicker
from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from .models import Leave

class LeaveForm(forms.Form):
    start_date = forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'))
    start_time = forms.TimeField(widget=TimePickerInput())
    end_date =  forms.DateField(widget=DatePickerInput(format='%d/%m/%Y'))
    end_time = forms.TimeField(widget=TimePickerInput())