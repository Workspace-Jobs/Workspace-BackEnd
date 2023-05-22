from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class USER(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    username = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    location = models.TextField()
    profile = models.ImageField(upload_to='profile/%Y/%m/%d', default='profile/default.png')

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RESUME(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resume/%Y/%m/%d')


class NOTICE_BOARD(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    title = models.TextField()
    centent = models.TextField()
    tag = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_data = models.DateTimeField(auto_now=True)


class COMMENT(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    nb = models.ForeignKey('NOTICE_BOARD', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    centent = models.TextField()


class GOOD(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    nb = models.ForeignKey('NOTICE_BOARD', on_delete=models.CASCADE)


class EMPLOYMENT(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.TextField()
    img1 = models.ImageField(upload_to='employment/%Y/%m/%d')
    img2 = models.ImageField(upload_to='employment/%Y/%m/%d', blank=True, null=True)
    img3 = models.ImageField(upload_to='employment/%Y/%m/%d', blank=True, null=True)
    centent = models.TextField()
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    date = models.DateField()
    B_job = models.TextField()
    job = models.TextField()


class SUPPORT(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    employment = models.ForeignKey('EMPLOYMENT', on_delete=models.CASCADE)
    resume = models.ForeignKey('RESUME', on_delete=models.CASCADE)
    state = models.TextField()


class MARK(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('USER', on_delete=models.CASCADE)
    employment = models.ForeignKey('EMPLOYMENT', on_delete=models.CASCADE)