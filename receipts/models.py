import datetime

from django.db import models


class Receipt(models.Model):
    store_name = models.TextField(max_length=250)
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date_of_purchase = models.DateField(default=datetime.date.today)
    item_list = models.TextField(max_length=500)