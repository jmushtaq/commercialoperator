# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-07-01 06:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('commercialoperator', '0116_park_visible_to_external'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='park',
            name='visible_to_external',
        ),
    ]
