# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-04-15 13:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commercialoperator', '0038_eventsparkdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbseilingClimbingActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leader', models.CharField(blank=True, max_length=255, null=True)),
                ('rego_number', models.CharField(blank=True, max_length=255, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('event_activities', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abseiling_climbing_activity_data', to='commercialoperator.ProposalEventActivities')),
                ('proposal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_abseiling_climbing_activity', to='commercialoperator.Proposal')),
            ],
        ),
    ]