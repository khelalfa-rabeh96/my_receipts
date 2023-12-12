from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Receipt

def receipts_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})

def new_receipt(request):
    if request.method == 'POST':
        total_amount = request.POST.get('new_total_amount', 0)
        Receipt.objects.create(total_amount=total_amount)
        return redirect(reverse('receipt-list'))

    return render(request, 'new_receipt.html')