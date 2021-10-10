"""Sklep URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from shop import views
from shop.models import Product, Client, Delivery, Basket, Order, ProductInOrder

from django.contrib.admin.sites import AlreadyRegistered

from shop.views import ProductDetailView, ProductUpdateView, ProductCreateView, ProductDeleteView, SignUpView, \
    SubmittableLoginView, SubmittablePasswordChangeForm, ProductView, OrderCreateView, AddOrderView

try:
    admin.site.register(Product)
    admin.site.register(Client)
    admin.site.register(Delivery)
    admin.site.register(Basket)
    admin.site.register(Order)
    admin.site.register(ProductInOrder)
except AlreadyRegistered:
    pass


urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('password_change/', SubmittablePasswordChangeForm.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('passwrod_reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('admin/', admin.site.urls),
    path('', ProductView.as_view(), name='products'),
    path('products/details/<id>', ProductDetailView.as_view(), name='product_details'),
    path('products/create/', ProductCreateView.as_view(), name='product_add'),
    path('products/delete/<pk>', ProductDeleteView.as_view(), name='product_delete'),
    path('products/update/<pk>', ProductUpdateView.as_view(), name='product_edit'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/add/<product_id>', AddOrderView.as_view(), name='order_add'),

    # path('basket/delete/<int:product_id>', views.basket_remove, name='basket_delete'),
    # path('basket/update/', BasketUpdateView.as_view(), name='basket_edit'),
    # path('purchse/', BasketUpdateView.as_view(), name='purchase'),
]
