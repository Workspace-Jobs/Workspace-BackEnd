from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from .models import *


class ResumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RESUME
        fields = ['id', 'user', 'resume']
        read_only_fields = ['id', 'user']


class NBDetailSerializers(serializers.ModelSerializer):
    good_cnt = serializers.SerializerMethodField()

    class Meta:
        model = NOTICE_BOARD
        fields = ['id', 'user', 'title', 'centent', 'tag', 'good_cnt', 'good_bool', 'created_date', 'updated_data']
        read_only_fields = ['id', 'user', 'good_cnt', 'good_bool', 'created_date', 'updated_data']

    def get_good_cnt(self, obj):
        O_list = GOOD.objects.filter(nb=obj)
        return len(O_list)


class NBListSerializers(serializers.ModelSerializer):
    good_cnt = serializers.SerializerMethodField()

    class Meta:
        model = NOTICE_BOARD
        fields = ['id', 'user', 'title', 'good_cnt', 'created_date']
        read_only_fields = ['id', 'user', 'title', 'good_cnt', 'created_date']

    def get_good_cnt(self, obj):
        G_list = GOOD.objects.filter(nb=obj)
        return len(G_list)


class COMMENTSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = COMMENT
        fields = ['id', 'user', 'nb', 'date', 'centent']
        read_only_fields = ['id', 'user', 'nb', 'date']

    def get_user(self, obj):
        user = obj.user
        return user.username
