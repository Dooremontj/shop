# Generated by Django 3.2 on 2021-08-29 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0031_basketresident'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='basket',
            options={'verbose_name': 'ligne de panier membre du personnel'},
        ),
        migrations.AlterModelOptions(
            name='basketresident',
            options={'verbose_name': 'ligne de panier résident'},
        ),
    ]