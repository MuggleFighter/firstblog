# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 08:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='label',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
