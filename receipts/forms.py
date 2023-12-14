from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Receipt

User = get_user_model()

class ReceiptModelForm(forms.ModelForm):
    total_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    item_list = forms.CharField(required=True)
    class Meta:
        model = Receipt
        fields = ['store_name', 'total_amount', 'item_list', 'date_of_purchase']


class RegisterModelFOrm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']
        exclude = ('password2',)
