from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView

from shop.models import Product


class ProductView(ListView):
    template_name = 'products.html'
    model = Product
