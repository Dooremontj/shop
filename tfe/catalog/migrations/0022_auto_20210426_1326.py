# Generated by Django 3.2 on 2021-04-26 11:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_auto_20210424_0653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 26, 13, 26, 53, 139362)),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.resident'),
        ),
    ]
