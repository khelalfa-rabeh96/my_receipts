from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views import View


from .models import Receipt
from .forms import ReceiptModelForm

def receipts_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})


class NewReceiptView(View):
    template_name = "new_receipt.html"

    def get(self, request, *args, **kwargs):
        form = ReceiptModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = ReceiptModelForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('receipts:receipt-list'))
        else:
            context = {"form": form}
            return render(request, self.template_name, context)
