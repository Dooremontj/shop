# Generated by Django 3.2 on 2021-08-25 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0023_auto_20210821_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limitfamily',
            name='limit_by_week',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('25', '25')], max_length=20, verbose_name='Limite par semaine'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_limit',
            field=models.CharField(choices=[('AUCUNE', 'AUCUNE'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('10', '10'), ('15', '15')], default='0', max_length=20, verbose_name='point(s)'),
        ),
    ]
