# Generated by Django 4.2.8 on 2023-12-12 19:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('receipts', '0006_alter_receipt_store_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='date_of_purchase',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
