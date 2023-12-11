from django.db import models

# Create your models here.
class Receipt(models.Model):
    total_amount = models.DecimalField(default=0, max_digits=10, decimal_places=2)