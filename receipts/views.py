from django.shortcuts import render

# Create your views here.
def receipts_list(request):
    return render(request, 'receipt_list.html')