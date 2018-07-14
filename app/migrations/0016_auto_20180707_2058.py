# Generated by Django 2.0.7 on 2018-07-07 18:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20180318_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='massschema',
            name='friday',
        ),
        migrations.RemoveField(
            model_name='massschema',
            name='monday',
        ),
        migrations.RemoveField(
            model_name='massschema',
            name='saturday',
        ),
        migrations.RemoveField(
            model_name='massschema',
            name='thursday',
        ),
        migrations.RemoveField(
            model_name='massschema',
            name='tuesday',
        ),
        migrations.RemoveField(
            model_name='massschema',
            name='wednesday',
        ),
        migrations.AlterField(
            model_name='actual',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 7, 20, 58, 38, 85252), verbose_name='data publikacji'),
        ),
        migrations.AlterField(
            model_name='massschema',
            name='sunday',
            field=models.BooleanField(default=False, verbose_name='Niedziela'),
        ),
        migrations.AlterField(
            model_name='officehours',
            name='end',
            field=models.TimeField(verbose_name='do godziny'),
        ),
        migrations.AlterField(
            model_name='officehours',
            name='start',
            field=models.TimeField(verbose_name='od godziny'),
        ),
    ]