# Generated by Django 4.2.8 on 2023-12-16 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('receipts', '0008_receipt_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipts', to=settings.AUTH_USER_MODEL),
        ),
    ]
