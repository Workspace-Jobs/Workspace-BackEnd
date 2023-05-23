from rest_framework import serializers
from datetime import date
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


class EMPLOYMENTDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = EMPLOYMENT
        fields = ['id', 'title', 'img1', 'img2', 'img3', 'centent', 'user', 'date', 'B_job', 'job']
        read_only_fields = ['id', 'user']


class EMPLOYMENTListByUSerSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['username', 'location']


class EMPLOYMENTListSerializers(serializers.ModelSerializer):
    user = EMPLOYMENTListByUSerSerializers()
    date = serializers.SerializerMethodField()

    class Meta:
        model = EMPLOYMENT
        fields = ['id', 'title', 'img1', 'user', 'date']
        read_only_fields = ['id', 'user']

    def get_date(self, obj):
        if obj.date == date(1111, 11, 11):
            return "상시"
        else:
            day = obj.date - date.today()
            if day.days == 0:
                return "D-day"
            return "D-"+str(day.days)

