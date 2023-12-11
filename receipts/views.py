from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Receipt

def receipts_list(request):
    if request.method == 'POST':
        total_amount = request.POST.get('new_total_amount', 0)
        Receipt.objects.create(total_amount=total_amount)
        return redirect(reverse('receipt-list'))
  
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})
