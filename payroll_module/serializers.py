from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Guard

class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
