from logging import getLogger

from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views import View
from django.views.decorators.http import require_POST

from shop import basket

LOGGER = getLogger()

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from shop.forms import ProductForm, SignUpForm, BasketAddProductForm, OrderForm
from shop.models import Product, Order
# from shop.basket import Basket


class ProductView(ListView):
    template_name = 'products.html'
    model = Product


class ProductCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'formAddEditProduct.html'
    form_class = ProductForm
    success_url = reverse_lazy('products')
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


class OrderCreateView(CreateView):
    template_name = 'order_create.html'
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('products')


class OrderView(View):
    def get(self, request):
       return render(
            request, 'order_details.html',
            context={'orders': Order.objects.all()}
        )


class AddOrderView(View):
    template_name = 'order_add.html'
    # model = Order
    # form_class = OrderForm
    success_url = reverse_lazy('products')

    def get(self, request, product_id):
        product = Product.objects.filter(id=product_id).first()
        order = Order.objects.get(id=request.GET.get("zamowienie_id"))
        order.products.add(product)
        order.save()






# @require_POST
# def basket_add(request, product_id):
#     basket = Basket(request)
#     product = get_object_or_404(Product, id=product_id)
#     form = BasketAddProductForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         basket.add(product=product, amount=cd['amount'], update_amount=cd['update'])
#     return redirect('basket:basket_detail')
#
#
# @require_POST
# def basket_remove(request, product_id):
#     basket = Basket(request)
#     product = get_object_or_404(Product, id=product_id)
#     basket.remove(product)
#     return redirect('basket:basket_detail')
#
#
# def basket_detail(request):
#     basket = Basket(request)
#     return render(request, 'basket_details.html', {'basket': basket})


# class BasketCreateView(PermissionRequiredMixin, CreateView):
#     template_name = 'formAddEditBasket.html'
#     form_class = Basket
#     success_url = reverse_lazy('basket_add')
#     permission_required = 'shop.basket_add'
#
#
# class BasketUpdateView(PermissionRequiredMixin, UpdateView):
#     template_name = 'formAddEditBasket.html'
#     form_class = Basket
#     success_url = reverse_lazy('basket_edit')
#     model = Basket
#     permission_required = 'shop.basket_edit'
#     LOGGER.warning('User provided invalid data')
#
#     def form_invalid(self, form):
#         LOGGER.warning('User provided invalid data')
#         return super().form_invalid(form)
#
#
# class BasketDeleteView(PermissionRequiredMixin, DeleteView):
#     template_name = 'basket_delete.html'
#     success_url = reverse_lazy('basket_delete')
#     model = Basket
#     permission_required = 'shop.basket_delete'
#
#
# class BasketDetailView(View):
#     def get(self, request, id):
#         return render(
#             request, 'basket_details.html',
#             context={'basket': Product.objects.get(id=id)}
#         )
#
#
# class PurchaseView(PermissionRequiredMixin, UpdateView):
#     template_name = 'fromAddEditBasket.html'
#     success_url = reverse_lazy('purchase')
#     model = Basket
#     permission_required = 'shop.purchase'
#
#
# class ProductClassificationView(PermissionRequiredMixin, UpdateView):
#     template_name = 'formAddEditProduct.html'
#     success_url = reverse_lazy('product_classification')
#     model = Basket
#     permission_required = 'shop.product_classification'
#
#
# class BasketDetailView(View):
#     def get(self, request, id):
#         return render(
#             request, 'baket_details.html',
#             context={'basket': Product.objects.get(id=id)}
#         )
