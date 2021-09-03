# Generated by Django 3.2 on 2021-09-03 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0034_fedorderitem_qty_supplied'),
    ]

    operations = [
        migrations.AddField(
            model_name='fedorder',
            name='prepared_by',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fedorder_prepared_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
