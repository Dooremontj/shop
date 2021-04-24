# Generated by Django 3.2 on 2021-04-24 04:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_auto_20210424_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 24, 6, 29, 43, 31613)),
        ),
        migrations.AlterField(
            model_name='resident',
            name='birthdate',
            field=models.DateTimeField(blank=True, max_length=100, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='datein',
            field=models.DateTimeField(blank=True, max_length=100, verbose_name="Date d'arrivée"),
        ),
    ]
