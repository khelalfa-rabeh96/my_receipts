from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,  get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Receipt
from .forms import ReceiptModelForm, RegisterModelForm, LoginForm


User = get_user_model()


def set_user_active(username):
    user = User.objects.filter(username=username).first()
    if (user) and (not user.is_active):
        user.is_active == True
        user.save()


def home(request):
    return redirect(reverse("receipts:receipt-list"))


def user_register(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            username = form.cleaned_data.get('username')
            set_user_active(username)
            return redirect(reverse('user-login'))
        else:
            messages.error(request, 'Some data is not valid')
    else:
        form = RegisterModelForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                messages.success(request, 'User logged-in successfully')
                return redirect(reverse('receipts:receipt-list'))
            else:
                messages.error(request, 'Username or password incorrect')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect(reverse('user-login'))

@login_required(login_url='user-login')
def receipts_list(request):
    receipts = Receipt.objects.filter(owner=request.user)
    return render(request, 'receipt_list.html', {'receipts': receipts})


class NewReceiptView(LoginRequiredMixin, View):
    template_name = "new_receipt.html"
    login_url = 'user-login'
    
    def get(self, request, *args, **kwargs):
        form = ReceiptModelForm()
        context = {"form": form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = ReceiptModelForm(request.POST or None)
        
        if form.is_valid():
            receipt = form.save(commit=False)
            receipt.owner = request.user
            receipt.save()
            messages.success(request, "An new receipt was created successfully.")
            return redirect(reverse('receipts:receipt-list'))
        else:
            messages.error(request, "Some data is not valid.")
            context = {"form": form}
            return render(request, self.template_name, context)


@login_required(login_url='user-login')
def receipt_detail_view(request, pk):
    if request.method == "GET":
        try:
            receipt = get_object_or_404(Receipt, pk=pk)
        except:
            return render(request, "404.html")
        
        return render(request, "receipt_detail.html", {"receipt": receipt})


# Get receipt object by pk or redirect to 404 page if not exists
class ReceiptMixinObject:
    def get_object(self, request):
        try:
            receipt = get_object_or_404(Receipt, pk=self.kwargs.get('pk'))
        except:
            return render(request, "404.html")
        
        return receipt

    
class ReceiptEditView(LoginRequiredMixin, View, ReceiptMixinObject):
    template_name = 'receipt_edit.html'
    login_url = 'user-login'

    def get(self, request, *args, **kwargs):
        receipt = self.get_object(request)
        form = ReceiptModelForm(instance=receipt)
        context = {"form": form, "receipt": receipt}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        receipt = self.get_object(request)
        form = ReceiptModelForm(request.POST or None, instance=receipt)

        if form.is_valid():
            form.save()
            messages.success(request, "This receipt was updated successfully.")
            return redirect(reverse('receipts:receipt-detail', kwargs={'pk': receipt.pk}))
        
        else:
            context = {"form": form}
            messages.warning(request, "Some data is not valid")
            return render(request, self.template_name, context)


class ReceiptDeleteView(LoginRequiredMixin, View, ReceiptMixinObject):
    tempalate_name = 'receipt_delete.html'
    login_url = 'user-login'
    
    def get(self, request, *args, **kwargs):
        receipt = self.get_object(request)
        context = {"receipt": receipt}
        return render(request, self.tempalate_name, context=context)
    
    def post(self, request, *args, **kwargs):
        receipt = self.get_object(request)
        receipt.delete()
        messages.success(request, "This receipt was deleted successfully.")
        return redirect(reverse('receipts:receipt-list'))