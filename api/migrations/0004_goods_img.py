# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-05-05 02:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_goods'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='img',
            field=models.CharField(max_length=256, null=True),
        ),
    ]
