# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricepaid', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='county',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='town',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
    ]
