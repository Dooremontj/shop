# Generated by Django 3.2 on 2021-08-21 07:12

import catalog.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0021_auto_20210424_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='FedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
                ('title', models.CharField(blank=True, max_length=150)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('OPEN', 'OPEN'), ('PARTIEL', 'PARTIEL'), ('CLOSED', 'CLOSED')], default='OPEN', max_length=20, verbose_name='Status de la commande')),
                ('order_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Commande - membre du personnel',
                'ordering': ['date', 'status'],
                'permissions': (('can_close_order', 'Fermer la commande'),),
            },
        ),
        migrations.CreateModel(
            name='LimitFamily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compo_family', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7')], max_length=20, verbose_name='Composition familiale')),
                ('limit_by_week', models.CharField(choices=[('AUCUNE', 'AUCUNE'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('25', '25')], max_length=20, verbose_name='Limite par semaine')),
            ],
        ),
        migrations.AlterModelOptions(
            name='resident',
            options={'ordering': ['badge', 'family_group', 'firstname'], 'verbose_name': 'Résident'},
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='qty',
        ),
        migrations.AddField(
            model_name='product',
            name='prod_child',
            field=models.BooleanField(default=False, verbose_name='Réservé aux familles avec enfants'),
        ),
        migrations.AddField(
            model_name='product',
            name='prod_limit',
            field=models.CharField(choices=[('AUCUNE', 'AUCUNE'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('10', '10'), ('15', '15')], default='AUCUNE', max_length=20, verbose_name='limite par semaine'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.resident'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_img',
            field=models.ImageField(blank=True, default='img/product/default_product.png', upload_to=catalog.models.content_file_name, verbose_name='Image du produit'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.supplier', verbose_name='Fournisseur'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='age',
            field=models.IntegerField(blank=True, verbose_name='Age'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='room',
            field=models.IntegerField(blank=True, verbose_name='Chambre'),
        ),
        migrations.CreateModel(
            name='FedOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.fedorder')),
            ],
            options={
                'verbose_name': 'ligne de commande - membre du personnel',
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=1)),
                ('error', models.CharField(max_length=200, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product')),
                ('user_basket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ligne de panier',
            },
        ),
    ]
