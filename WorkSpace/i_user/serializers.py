from rest_framework import serializers
from .models import *


class ResumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RESUME
        fields = ['id', 'user', 'resume']
        read_only_fields = ['id', 'user']
