# Generated by Django 3.1.7 on 2021-04-15 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobapp', '0010_add_applied_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resumebuilder',
            old_name='end_date',
            new_name='experience_year',
        ),
        migrations.RemoveField(
            model_name='resumebuilder',
            name='start_date',
        ),
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 15, 12, 7, 15, 869139)),
        ),
    ]