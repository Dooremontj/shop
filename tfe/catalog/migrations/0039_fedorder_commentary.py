# Generated by Django 3.2 on 2021-09-03 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0038_fedorderitem_already_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='fedorder',
            name='commentary',
            field=models.TextField(blank=True, default='', verbose_name='Commentaire'),
        ),
    ]