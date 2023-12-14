from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.views import View
from django.contrib import messages


from .models import Receipt
from .forms import ReceiptModelForm

def home(request):
    return redirect(reverse("receipts:receipt-list"))

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
        try:
            receipt = get_object_or_404(Receipt, pk=pk)
        except:
            return render(request, "404.html")
        
        return render(request, "receipt_detail.html", {"receipt": receipt})


class ReceiptEditView(View):
    def get(self, request, *args, **kwargs):
        try:
            receipt = get_object_or_404(Receipt, pk=self.kwargs.get('pk'))
        except:
            return render(request, "404.html")

        form = ReceiptModelForm(instance=receipt)
        context = {"form": form, "receipt": receipt}
        return render(request, 'receipt_edit.html', context)

    def post(self, request, *args, **kwargs):
        try:
            receipt = get_object_or_404(Receipt, pk=self.kwargs.get('pk'))
        except:
            return render(request, "404.html")

        form = ReceiptModelForm(request.POST or None, instance=receipt)

        if form.is_valid():
            form.save()
            messages.success(request, "This receipt was updated successfully.")
            return redirect(reverse('receipts:receipt-detail', kwargs={'pk': receipt.pk}))
        
        else:
            context = {"form": form}
            messages.warning(request, "Some data is not valid")
            return render(request, self.template_name, context)