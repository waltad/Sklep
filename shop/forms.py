from logging import getLogger

from django.contrib.auth.forms import UserCreationForm
from django.db.models import TextField
from django.db.transaction import atomic

LOGGER = getLogger()
from django.forms import (
    ModelForm, CharField, ModelChoiceField, IntegerField, DateField, Textarea, DecimalField, Form, TypedChoiceField,
    BooleanField, HiddenInput
)

from shop.models import Product, Client, Delivery, Basket, Order, ProductInOrder, Profile

# from viewer.validators import PastMonthField, capitalized_validator
from django.core.exceptions import ValidationError

import re

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class BasketAddProductForm(Form):
    quantity = TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = BooleanField(required=False, initial=False, widget=HiddenInput)


class ProductForm(ModelForm):
    class Meta:  # subklasa opisująca dane z których będzie tworzy form
        model = Product  # model na podstawie tworzymy formularz
        fields = '__all__'  # wykorzystujemy wszystkie pola z modelu

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        # pobranie wartości pola description
        initial = self.cleaned_data['description']
        # podział tekstu na części "od kropki do kropki" na zdania
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        # zamina na wielką literę pierwszj litery każdego ze zdań,
        # dodanie kropki, powtórzenie operacji dla kolejnego zdania
        return '.'.join(sentence.capitalize() for sentence in sentences)


class OrderForm(ModelForm):
    class Meta:  # subklasa opisująca dane z których będzie tworzy form
        model = Order  # model na podstawie tworzymy formularz
        fields = '__all__'  # wykorzystujemy wszystkie pola z modelu

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    street = CharField(
        label='Podaj ulicę', min_length=3, max_length=128
    )
    home_number = CharField(
        label='Podaj numer domu', min_length=1
    )
    flat_number = CharField(
        label='Podaj numer mieszkania', min_length=1
    )
    postcode = CharField(
        label='Podaj kod pocztowy', min_length=5
    )
    locality = CharField(
        label='Podaj miejscowość zamieszkania', min_length=3
    )
    country = CharField(
        label='Podaj kraj zamieszkania', min_length=3
    )
    phone_number = CharField(
        label='Podaj numer telefonu', min_length=3
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_activate = False
        result = super().save(commit)
        street = self.cleaned_data['street']
        home_number = self.cleaned_data['home_number']
        flat_number = self.cleaned_data['flat_number']
        postcode = self.cleaned_data['postcode']
        locality = self.cleaned_data['locality']
        country = self.cleaned_data['country']
        phone_number = self.cleaned_data['phone_number']
        profile = Profile(street=street, home_number=home_number, flat_number=flat_number, postcode=postcode,
                          locality=locality, country=country, phone_number=phone_number, user=result)
        if commit:
            profile.save()
        return result


# class BasketForm(ModelForm):
#     class Meta:  # subklasa opisująca dane z których będzie tworzy form
#         model = Basket  # model na podstawie tworzymy formularz
#         fields = '__all__'  # wykorzystujemy wszystkie pola z modelu
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
