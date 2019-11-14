#from bootstrap4_datetime.widgets import DateTimePicker
from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

class LeaveDateTime(forms.Form):

    startdate = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )

    starttime = forms.DateTimeField(
        widget=TimePickerInput
    )

    enddate = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y')
    )

    endtime = forms.DateTimeField(
        widget=TimePickerInput
    )


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()