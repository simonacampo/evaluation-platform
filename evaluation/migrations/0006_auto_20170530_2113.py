# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-30 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0005_auto_20170529_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='score',
            field=models.SmallIntegerField(),
        ),
    ]
