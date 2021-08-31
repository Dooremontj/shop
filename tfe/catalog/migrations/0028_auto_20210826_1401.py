# Generated by Django 3.2 on 2021-08-26 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_alter_limitfamily_point_by_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='points',
            field=models.IntegerField(default='0', verbose_name='points'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_limit',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (10, 10), (15, 15)], default=0, max_length=20, verbose_name='point(s)'),
        ),
    ]