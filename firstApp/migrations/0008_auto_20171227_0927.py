# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 09:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0007_auto_20171227_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='Match_Date',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='player',
            name='DOB',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
