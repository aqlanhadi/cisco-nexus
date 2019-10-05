#from bootstrap4_datetime.widgets import DateTimePicker
from django import forms
from bootstrap_datepicker_plus import DateTimePickerInput

class LeaveDateTime(forms.Form):
    
    date = forms.DateField(
        widget=DateTimePickerInput(format='%m/%d/%Y')
    )
    