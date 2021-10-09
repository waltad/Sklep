from decimal import Decimal

from Sklep import settings
from shop.models import Product


class Basket(object):
    def __init__(self, request):
        # Inicjalizacja koszyka na zakupy.
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if not basket:
        # Zapis pustego koszyka na zakupy w sesji.
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, amount=1, update_amount=False):
        # Dodanie produktu do koszyka lub zmiana jego ilości.
        product_id = str(product.id)
        if product_id not in self.basket:
            self.basket[product_id] = {'amount': 0, 'price': str(product.price)}
        if update_amount:
            self.basket[product_id]['amount'] = amount
        else:
            self.basket[product_id]['amount'] += amount
        self.save()

    def remove(self, product):
        # Usunięcie produktu z koszyka na zakupy.

        product_id = str(product.id)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def __iter__(self):
        # Iteracja przez elementy koszyka na zakupy i pobranie produktów z bazy danych.

        product_ids = self.basket.keys()
        # Pobranie obiektów produktów i dodanie ich do koszyka na zakupy.
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['amount']
            yield item

    def __len__(self):
        # Obliczenie liczby wszystkich elementów w koszyku na zakupy.
        return sum(item['quantity'] for item in self.basket.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.basket.values())
