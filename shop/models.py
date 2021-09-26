from django.db.models import (Model,
                              CharField, DateField, DateTimeField, IntegerField, DecimalField, TextField,
                              ForeignKey, DO_NOTHING, )
# Create your models here.


class Product(Model):
    category = CharField(max_length=128)
    photo = CharField(max_length=128)
    description = TextField(null=True)
    amount = IntegerField(default=0)
    price = DecimalField(max_digits=10, decimal_places=2)


class Client(Model):
    name = CharField(max_length=128)
    surname = CharField(max_length=128)
    street = CharField(max_length=128)
    home_number = CharField(max_length=128)
    flat_number = CharField(max_length=128)
    postcode = CharField(max_length=128)
    locality = CharField(max_length=128)
    country = CharField(max_length=128)
    mail = CharField(max_length=128)
    phone_number = CharField(max_length=128)


class Delivery(Model):
    delivery_company = CharField(max_length=128)
    delivery_price = DecimalField(max_digits=5, decimal_places=2)


class Basket(Model):
    product = ForeignKey(Product, on_delete=DO_NOTHING)
    amount = IntegerField(default=0)
    client = ForeignKey(Client, on_delete=DO_NOTHING)


class Order(Model):
    delivery = ForeignKey(Delivery, on_delete=DO_NOTHING)
    client = ForeignKey(Client, on_delete=DO_NOTHING)
    date_order = DateTimeField(auto_now_add=True)


class ProductInOrder(Model):
    order = ForeignKey(Order, on_delete=DO_NOTHING)
    product = ForeignKey(Product, on_delete=DO_NOTHING)
    amount = IntegerField(default=0)
