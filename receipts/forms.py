from django import forms
from django.core.exceptions import ValidationError

from .models import Receipt

class ReceiptModelForm(forms.ModelForm):
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    item_list = forms.CharField(required=True)
    class Meta:
        model = Receipt
        fields = ['store_name', 'total_amount', 'item_list']