from rest_framework import serializers
from .models import Entry

class ShiftSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(source='start_datetime')
    end = serializers.DateTimeField(source='end_datetime')

    class Meta:
        model = Entry
        fields = ['start', 'end']