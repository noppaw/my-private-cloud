from rest_framework import serializers
from .models import MicroApp

class MicroAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = MicroApp
        fields = ['id', 'title', 'description', 'url', 'icon_name']