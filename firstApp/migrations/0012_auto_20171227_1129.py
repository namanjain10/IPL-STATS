# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-27 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0011_auto_20171227_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ball_by_ball',
            name='Dissimal_Type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ball_by_ball',
            name='Extra_Runs',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ball_by_ball',
            name='Extra_Type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ball_by_ball',
            name='Fielder_Id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ball_by_ball',
            name='Player_dissimal_Id',
            field=models.IntegerField(null=True),
        ),
    ]
