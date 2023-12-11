from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def receipts_list(request):
    
    return render(request, 'receipt_list.html', {
    'new_total_amount': request.POST.get('new_total_amount', ''),
    })