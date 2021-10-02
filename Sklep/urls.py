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
from django.contrib.auth.views import LogoutView
from django.urls import path

from shop import views
from shop.models import Product, Client, Delivery, Basket, Order, ProductInOrder

from django.contrib.admin.sites import AlreadyRegistered

from shop.views import ProductDetailView, SubmittableLoginView, SubmittablePasswordChangeForm

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
    path('admin/', admin.site.urls),
    path('', views.ProductView.as_view(), name='products'),
    path('products/details/<id>', ProductDetailView.as_view(), name='movie_details'),
]
