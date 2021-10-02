from logging import getLogger

from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views import View

LOGGER = getLogger()

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from shop.forms import ProductForm, SignUpForm
from shop.models import Product


class ProductView(ListView):
    template_name = 'products.html'
    model = Product


class MovieCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'formAddEditProduct.html'
    form_class = ProductForm
    success_url = reverse_lazy('product_add')
    permission_required = 'shop.product_add'

    # co dzieje się, gdy formularz nie przejdzie walidacji:
    def form_invalid(self, form):
        # odkładamy w logach informacje o operacji
        LOGGER.warning('User provided invalid data')
        # zwraca wynik działania pierwotnej funkcji form_invalid
        return super().form_invalid(form)


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'formAddEditProduct.html'
    form_class = ProductForm
    # adres pobrany z UrLs który zostaniemy przekierowanina
    # gdy aktualizacja się powiedzie (index pochodzi z name!)
    success_url = reverse_lazy('products')
    # Nazwa encji z której będziemy
    model = Product
    permission_required = 'shop.product_edit'
    LOGGER.warning('User provided invalid data')

    # co dzieje się, gdy formularz nie przejdzie walidacji:
    def form_invalid(self, form):
        # odkładamy w logach informacje o operacji
        LOGGER.warning('User provided invalid data')
        # zwraca wynik działania pierwotnej funkcji form_invalid
        return super().form_invalid(form)


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    template_name = 'product_delete.html'
    success_url = reverse_lazy('products')
    # Nazwa necji z której będziemy kasować rekord
    model = Product
    permission_required = 'shop.product_delete'


class ProductDetailView(View):
    def get(self, request, id):
        return render(
            request, 'product_details.html',
            context={'products': Product.objects.get(id=id)}
        )


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SubmittablePasswordChangeForm(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('products')


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'form.html'
    success_url = reverse_lazy('products')
