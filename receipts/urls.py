from django.urls import path

from .views import receipts_list, NewReceiptView, receipt_detail_view, ReceiptEditView

app_name = "receipts"

urlpatterns = [
    path('', receipts_list, name="receipt-list"),
    path('new', NewReceiptView.as_view(), name="new-receipt"),
    path('<int:pk>', receipt_detail_view, name="receipt-detail"),
    path('<int:pk>/edit', ReceiptEditView.as_view(), name="receipt-edit")
]
