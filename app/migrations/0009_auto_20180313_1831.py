# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-13 17:31
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180310_2112'),
    ]

    operations = [
        migrations.CreateModel(
            name='MassSchema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='nazwa sezonu')),
                ('season_start', models.DateField(blank=True, null=True, verbose_name='Pierwszy dzień sezonu')),
                ('season_end', models.DateField(blank=True, null=True, verbose_name='Ostatni dzień sezonu')),
            ],
            options={
                'verbose_name': 'Lista mszy w sezonie',
                'verbose_name_plural': 'Schemat mszy',
            },
        ),
        migrations.CreateModel(
            name='WeekOfMass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.CharField(blank=True, choices=[('Poniedziałek', 'Poniedziałek'), ('Wtorek', 'Wtorek'), ('Środa', 'Środa'), ('Czwartek', 'Czwartek'), ('Piątek', 'Piątek'), ('Sobota', 'Sobota'), ('Niedziela', 'Niedziela')], max_length=12, null=True, verbose_name='Dzień tygodnia')),
                ('mass_chema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.MassSchema', verbose_name='Lista mszy w sezonie')),
            ],
        ),
        migrations.AlterModelOptions(
            name='hour',
            options={'verbose_name': 'godzina mszy', 'verbose_name_plural': 'godziny mszy'},
        ),
        migrations.AddField(
            model_name='hour',
            name='church',
            field=models.CharField(blank=True, choices=[('św. Faustyny', 'św. Faustyny'), ('Miłosierdzia Bożego', 'Miłosierdzia Bożego')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='actual',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 13, 18, 31, 17, 825639), verbose_name='data publikacji'),
        ),
        migrations.AlterField(
            model_name='hour',
            name='mass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.WeekOfMass', verbose_name='msza'),
        ),
        migrations.DeleteModel(
            name='Mass',
        ),
    ]