# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-12 18:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailstreamfieldforms', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissionfield',
            name='field_type',
        ),
    ]
