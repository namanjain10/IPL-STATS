# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-12 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0013_auto_20171228_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='url',
            field=models.URLField(blank=True),
        ),
    ]
