from django.urls import path

from .views import receipts_list, new_receipt, NewReceiptView

app_name = "receipts"

urlpatterns = [
    path('', receipts_list, name="receipt-list"),
    path('new', NewReceiptView.as_view(), name="new-receipt"),
]
