# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-19 08:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_maatschappelijkeactiviteit_nonmailing'),
    ]

    operations = [
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='fulltimeWerkzamePersonen',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='parttimeWerkzamePersonen',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='maatschappelijkeactiviteit',
            name='totaalWerkzamePersonen',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True),
        ),
    ]