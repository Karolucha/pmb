# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-20 20:16
from __future__ import unicode_literals

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', app.models.ListField()),
                ('church', models.CharField(max_length=50)),
                ('season_name', models.CharField(max_length=20, verbose_name='nazwa sezonu')),
                ('season_start', models.DateField()),
                ('season_end', models.DateField(verbose_name='Ostatni dzień sezonu')),
            ],
        ),
    ]
