from rest_framework import serializers
from datetime import date

from .models import *


class ResumeSerializers(serializers.ModelSerializer):
    class Meta:
        model = RESUME
        fields = ['id', 'user', 'name', 'resume']
        read_only_fields = ['id', 'user']


class ResumeListSerializers(serializers.ModelSerializer):
    class Meta:
        model = RESUME
        fields = ['id', 'user', 'name']
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


class EMPLOYMENTListByUSerSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['id', 'username', 'location']


class EMPLOYMENTListSerializers(serializers.ModelSerializer):
    user = EMPLOYMENTListByUSerSerializers()
    date = serializers.SerializerMethodField()

    class Meta:
        model = EMPLOYMENT
        fields = ['id', 'title', 'img1', 'user', 'date']
        read_only_fields = ['id', 'user']

    def get_date(self, obj):
        if obj.date == date(9999, 12, 30):
            return "상시"
        else:
            day = obj.date - date.today()
            if day.days == 0:
                return "D-day"
            return "D-" + str(day.days)


class EMPLOYMENTDetailSerializers(serializers.ModelSerializer):
    user = EMPLOYMENTListByUSerSerializers()
    date = serializers.SerializerMethodField()
    support_bool = serializers.BooleanField()

    class Meta:
        model = EMPLOYMENT
        fields = ['id', 'title', 'img1', 'img2', 'img3', 'centent', 'support_bool', 'user', 'date', 'B_job', 'job']
        read_only_fields = ['id', 'user']

    def get_date(self, obj):
        if obj.date == date(9999, 12, 30):
            return "상시"
        else:
            return obj.date


class SUPPORTSerializers(serializers.ModelSerializer):
    resume = serializers.IntegerField()

    class Meta:
        model = SUPPORT
        fields = ['id', 'resume', 'phone', 'email']
        read_only_fields = ['id']


class USERMyPageSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['id', 'email', 'profile']
        read_only_fields = ['id', 'email', 'profile']


class MyPageMarkSerializers(serializers.ModelSerializer):
    employment = EMPLOYMENTListSerializers()

    class Meta:
        model = MARK
        fields = ['id', 'employment']
        read_only_fields = ['id', 'employment']


class MyPageGoodSerializers(serializers.ModelSerializer):
    nb = NBListSerializers()

    class Meta:
        model = GOOD
        fields = ['id', 'nb']
        read_only_fields = ['id', 'nb']


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['profile']


class UserNameSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['username']


class UserMainSerializers(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ['username', 'profile']


class EmploymentMyPageSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = EMPLOYMENT
        fields = ['id', 'title', 'user']

    def get_user(self, obj):
        return obj.user.username


class SUPPORTListSerializers(serializers.ModelSerializer):
    employment = EmploymentMyPageSerializers()

    class Meta:
        model = SUPPORT
        fields = ['id', 'employment', 'date']


class EmploymentMyPageDetailSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = EMPLOYMENT
        fields = ['id', 'title', 'user']

    def get_user(self, obj):
        return obj.user.username


class ResumeBySerializers(serializers.ModelSerializer):
    class Meta:
        model = RESUME
        fields = ['id', 'name', 'resume']
        read_only_fields = ['id']


class SUPPORTDetailSerializers(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    employment = EmploymentMyPageSerializers()
    resume = ResumeBySerializers()

    class Meta:
        model = SUPPORT
        fields = ['id', 'user', 'employment', 'resume', 'email', 'phone']

    def get_user(self, obj):
        return obj.user.username
