from django.db import models

# Create your models here.
class Receipt(models.Model):
    store_name = models.TextField(max_length=250)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    item_list = models.TextField(max_length=500)