# Generated by Django 3.2 on 2021-09-03 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0037_fedorderitem_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='fedorderitem',
            name='already_delivered',
            field=models.BooleanField(default=False),
        ),
    ]
