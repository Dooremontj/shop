# Generated by Django 3.2 on 2021-08-29 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_auto_20210826_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prd_main_category',
            field=models.CharField(choices=[('RESIDENT', 'RESIDENT'), ('PERSONNEL', 'PERSONNEL')], default='PERSONNEL', max_length=20, verbose_name='Catégorie'),
        ),
    ]
