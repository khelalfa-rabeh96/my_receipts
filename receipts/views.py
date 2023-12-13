from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views import View
from django.contrib import messages


from .models import Receipt
from .forms import ReceiptModelForm

def receipts_list(request):
    receipts = Receipt.objects.all()
    return render(request, 'receipt_list.html', {'receipts': receipts})


class NewReceiptView(View):
    template_name = "new_receipt.html"

    def get(self, request, *args, **kwargs):
        form = ReceiptModelForm()
        _messages = messages.get_messages(request)
        context = {"form": form, "messages": _messages}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = ReceiptModelForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "An new receipt was created successfully.")
            _messages = messages.get_messages(request)
            return redirect(reverse('receipts:receipt-list'),  kwargs={"messages": _messages})
        else:
            messages.error(request, "Some data is not valid.")
            context = {"form": form}
            return render(request, self.template_name, context)


def receipt_detail_view(request, pk):
    if request.method == "GET":
        receipt = get_object_or_404(Receipt, pk=pk)
        return render(request, "receipt_detail.html", {"receipt": receipt})