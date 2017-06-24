# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-23 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20170623_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(related_name='follower', to='authentication.Profile'),
        ),
    ]
