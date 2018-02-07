# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-04 15:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.TimeField(verbose_name='godzina mszy')),
            ],
        ),
        migrations.AlterField(
            model_name='mass',
            name='hours',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Hour'),
        ),
    ]
