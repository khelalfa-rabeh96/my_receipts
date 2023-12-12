from django.urls import path

from .views import receipts_list, new_receipt

urlpatterns = [
    path('', receipts_list, name="receipt-list"),
    path('new', new_receipt, name="new-receipt"),
]
