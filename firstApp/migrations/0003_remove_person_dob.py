# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-25 21:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0002_auto_20171225_2130'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='dob',
        ),
    ]
