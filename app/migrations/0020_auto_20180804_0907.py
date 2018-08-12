# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-04 07:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20180804_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='MassSchemaRows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sunday', models.BooleanField()),
                ('church', models.CharField(max_length=30, verbose_name=(('f', 'św. Faustyny'), ('mb', 'Miłosierdzia Bożego')))),
                ('hours', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='actual',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 4, 9, 7, 58, 268473), verbose_name='data publikacji'),
        ),
    ]
