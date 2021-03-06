# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-26 22:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0003_remove_person_dob'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='company',
            name='person',
        ),
        migrations.RemoveField(
            model_name='person',
            name='id',
        ),
        migrations.RemoveField(
            model_name='person',
            name='name',
        ),
        migrations.AddField(
            model_name='person',
            name='dob',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='person',
            name='person_id',
            field=models.IntegerField(default=None, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='person',
            name='person_name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.AddField(
            model_name='office',
            name='person_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='firstApp.Person'),
        ),
    ]
