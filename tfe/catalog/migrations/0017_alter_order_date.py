# Generated by Django 3.2 on 2021-04-24 04:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20210423_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 24, 6, 8, 31, 871971)),
        ),
    ]