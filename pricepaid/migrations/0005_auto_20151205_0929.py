# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pricepaid', '0004_auto_20151205_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pricepaidentry',
            name='postcode',
            field=models.CharField(max_length=8, db_index=True),
        ),
        migrations.AlterField(
            model_name='pricepaidentry',
            name='price',
            field=models.PositiveIntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='pricepaidentry',
            name='property_type',
            field=models.IntegerField(default=4, db_index=True),
        ),
        migrations.AlterField(
            model_name='pricepaidentry',
            name='transfer_date',
            field=models.DateTimeField(db_index=True),
        ),
    ]
