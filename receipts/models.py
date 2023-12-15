import datetime

from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def user_to_inactive(sender, instance, created, update_fields, **kwargs):
    if created:
        instance.is_active = True

class Receipt(models.Model):
    store_name = models.TextField(max_length=250)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date_of_purchase = models.DateField(default=datetime.date.today)
    item_list = models.TextField(max_length=500)