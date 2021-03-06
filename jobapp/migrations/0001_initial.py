# Generated by Django 3.0 on 2020-11-05 07:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields
import jobapp.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='employer')),
                ('website', models.CharField(max_length=100)),
                ('compnay', models.CharField(max_length=100)),
                ('company_image', models.ImageField(upload_to='employer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='job')),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contact', 'Contact'), ('internship', 'Internship')], max_length=100)),
                ('level', models.CharField(choices=[('junior', 'Junior'), ('mid', 'Mid'), ('seneior', 'Seneior')], max_length=50)),
                ('deadline', models.DateTimeField(default=datetime.datetime(2020, 11, 5, 13, 34, 1, 1221))),
                ('vaccncy_number', models.PositiveIntegerField()),
                ('education', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('experience', models.CharField(blank=True, max_length=100, null=True)),
                ('salary', models.CharField(blank=True, max_length=100, null=True)),
                ('views_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='jobcategory')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='jobseeker')),
                ('qualification', models.CharField(max_length=100)),
                ('skills', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('cv', models.FileField(upload_to='jobseeker', validators=[jobapp.validators.validate_file])),
                ('user', models.OneToOneField(on_delete=django.db.models.fields.CharField, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cover_letter', models.FileField(upload_to='jobapplication')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.Job')),
                ('jobseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.JobSeeker')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='job',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.JobCategory'),
        ),
        migrations.AddField(
            model_name='job',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobapp.Employer'),
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mobile', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='admin')),
                ('name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
