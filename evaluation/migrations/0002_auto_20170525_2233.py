# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 22:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evaluation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='url',
            field=models.URLField(help_text='This is the link that people evaluating the platform will go to'),
        ),
        migrations.AlterField(
            model_name='question',
            name='explanation',
            field=models.TextField(blank=True, help_text='To help clarify how to answer the question'),
        ),
    ]
