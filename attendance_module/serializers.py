from rest_framework import serializers
from .models import Entry

class ShiftSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    start = serializers.DateTimeField(source='start_datetime')
    end = serializers.DateTimeField(source='end_datetime')
    backgroundColor = serializers.SerializerMethodField('color')
    className = serializers.SerializerMethodField('class_name')

    def color(self, col):
        color = self.context.get("color")
        return color

    def class_name(self, class_name):
        class_name = self.context.get("class")
        return class_name

    class Meta:
        model = Entry
        fields = ['id', 'start', 'end', 'backgroundColor', 'className']