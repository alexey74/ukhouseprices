# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('county', models.ForeignKey(to='pricepaid.County')),
            ],
        ),
        migrations.CreateModel(
            name='PricePaidEntry',
            fields=[
                ('id', models.UUIDField(serialize=False, primary_key=True)),
                ('price', models.PositiveIntegerField()),
                ('transfer_date', models.DateTimeField()),
                ('postcode', models.CharField(max_length=8)),
                ('property_type', models.IntegerField(default=4)),
            ],
        ),
        migrations.CreateModel(
            name='Town',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('district', models.ForeignKey(to='pricepaid.District')),
            ],
        ),
        migrations.AddField(
            model_name='pricepaidentry',
            name='town',
            field=models.ForeignKey(to='pricepaid.Town'),
        ),
    ]
