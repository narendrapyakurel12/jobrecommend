# Generated by Django 3.1.7 on 2021-04-11 06:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0009_auto_20210406_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='compnay',
            field=models.CharField(default=datetime.datetime(2021, 4, 11, 6, 8, 18, 779930, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobapplication',
            name='is_applied',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 11, 11, 53, 7, 447862)),
        ),
    ]
