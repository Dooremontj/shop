# Generated by Django 3.2 on 2021-08-29 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0029_product_prd_main_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='prd_main_category',
            new_name='prod_main_category',
        ),
    ]
