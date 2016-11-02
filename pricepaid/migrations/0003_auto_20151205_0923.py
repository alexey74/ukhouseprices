# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricepaid', '0002_auto_20151205_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='town',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
