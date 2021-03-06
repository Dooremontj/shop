# Generated by Django 3.2 on 2021-04-23 13:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20210422_1238'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resident',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge', models.IntegerField(blank=True, verbose_name='Badge')),
                ('family_group', models.CharField(blank=True, max_length=2, verbose_name='Composition familiale')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Nom')),
                ('firstname', models.CharField(blank=True, max_length=100, verbose_name='Prénom')),
                ('room', models.CharField(blank=True, max_length=5, verbose_name='Chambre')),
                ('birthdate', models.DateField(blank=True, verbose_name='Date de naissance')),
                ('age', models.PositiveIntegerField(blank=True, verbose_name='Age')),
                ('datein', models.DateField(blank=True, verbose_name="Date d'arrivée")),
                ('sexe', models.CharField(blank=True, max_length=1, verbose_name='Sexe')),
            ],
            options={
                'verbose_name': 'Résident',
                'ordering': ['badge'],
            },
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 23, 15, 21, 57, 367915)),
        ),
    ]
