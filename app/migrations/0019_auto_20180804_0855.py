# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-04 06:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20180801_1659'),
    ]

    operations = [
        migrations.CreateModel(
            name='SectionRows',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_kind', models.CharField(max_length=50)),
                ('row_content', models.CharField(max_length=500)),
            ],
        ),
        migrations.AlterField(
            model_name='actual',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 4, 8, 55, 56, 317471), verbose_name='data publikacji'),
        ),
    ]