# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-01 12:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0008_dataselectie_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataselectie',
            old_name='vestiging_id',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='geovestigingen',
            name='sbi_detail_group',
            field=models.CharField(blank=True, db_index=True, help_text='De codering van de activiteit conform de SBI2008', max_length=200, null=True),
        ),
    ]