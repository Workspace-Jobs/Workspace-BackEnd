# Generated by Django 4.2.1 on 2023-05-22 03:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='USER',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('username', models.TextField()),
                ('is_staff', models.BooleanField(default=False)),
                ('is_company', models.BooleanField(default=False)),
                ('location', models.TextField()),
                ('profile', models.ImageField(default='profile/default.png', upload_to='profile/%Y/%m/%d')),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EMPLOYMENT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('img1', models.ImageField(upload_to='employment/%Y/%m/%d')),
                ('img2', models.ImageField(blank=True, null=True, upload_to='employment/%Y/%m/%d')),
                ('img3', models.ImageField(blank=True, null=True, upload_to='employment/%Y/%m/%d')),
                ('centent', models.TextField()),
                ('date', models.DateField()),
                ('B_job', models.TextField()),
                ('job', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RESUME',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resume', models.FileField(upload_to='resume/%Y/%m/%d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SUPPORT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('state', models.TextField()),
                ('employment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i_user.employment')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i_user.resume')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NOTICE_BOARD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.TextField()),
                ('centent', models.TextField()),
                ('tag', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_data', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MARK',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('employment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i_user.employment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GOOD',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i_user.notice_board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='COMMENT',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('centent', models.TextField()),
                ('nb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='i_user.notice_board')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
