from django.db import models
from django.db.models import (Model,
                              CharField, DateField, DateTimeField, IntegerField, TextField,
                              ForeignKey, DO_NOTHING, )
# Create your models here.

class Product(Model):
    category = CharField(max_length=128)
    photo = CharField(max_length=128)
    description = TextField
    amount = IntegerField
    price = models.DecimalField(max_digits=10,decimal_places=2)


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
    delivery_price = models.DecimalField(max_digits=5,decimal_places=2)


class Basket(Model):
    product = ForeignKey(Product)
    amount = IntegerField
    client = ForeignKey(Client)


class Order(Model):
    delivery = ForeignKey(Delivery)
    client = ForeignKey(Client)
    date_order = DateTimeField(auto_created=True)


class Product_in_order(Model):
    product =
    order = ForeignKey(Order)
    product = ForeignKey(Product)
    amount = IntegerField








