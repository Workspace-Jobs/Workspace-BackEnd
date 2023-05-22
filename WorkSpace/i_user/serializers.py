from rest_framework import serializers
from .models import *


class ResumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RESUME
        fields = ['id', 'user', 'resume']
        read_only_fields = ['id', 'user']


class NBDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = NOTICE_BOARD
        fields = ['id', 'user', 'title', 'centent', 'tag', 'created_date', 'updated_data']
        read_only_fields = ['id', 'user', 'created_date', 'updated_data']


class NBListSerializers(serializers.ModelSerializer):
    good_cnt = serializers.SerializerMethodField()

    class Meta:
        model = NOTICE_BOARD
        fields = ['id', 'user', 'title', 'good_cnt', 'created_date']
        read_only_fields = ['id', 'user', 'title', 'good_cnt', 'created_date']

    def get_good_cnt(self, obj):
        O_list = GOOD.objects.filter(NOTICE_BOARD=obj)
        return len(O_list)
