# Generated by Django 3.2 on 2021-04-23 16:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_alter_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 23, 18, 59, 34, 806944)),
        ),
        migrations.AlterField(
            model_name='resident',
            name='birthdate',
            field=models.CharField(blank=True, max_length=100, verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='datein',
            field=models.CharField(blank=True, max_length=100, verbose_name="Date d'arrivée"),
        ),
    ]
