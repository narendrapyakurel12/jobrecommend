# Generated by Django 3.1.7 on 2021-04-03 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0005_auto_20210403_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 3, 15, 47, 45, 792395)),
        ),
        migrations.AlterField(
            model_name='resumebuilder',
            name='end_date',
            field=models.CharField(help_text='year/month/day', max_length=100),
        ),
        migrations.AlterField(
            model_name='resumebuilder',
            name='start_date',
            field=models.CharField(help_text='year/month/day', max_length=100),
        ),
    ]
