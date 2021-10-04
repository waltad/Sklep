from logging import getLogger

from django.contrib.auth.forms import UserCreationForm
from django.db.models import TextField
from django.db.transaction import atomic

LOGGER = getLogger()
from django.forms import (
    ModelForm, CharField, ModelChoiceField, IntegerField, DateField, Textarea, DecimalField
)

from shop.models import Product, Client, Delivery, Basket, Order, ProductInOrder, Profile

# from viewer.validators import PastMonthField, capitalized_validator
from django.core.exceptions import ValidationError

import re


class ProductForm(ModelForm):
    class Meta: #subklasa opisująca dane z których będzie tworzy form
        model = Product #model na podstawie tworzymy formularz
        fields = '__all__' #wykorzystujemy wszystkie pola z modelu

    #pola z własnymi walidatorami dodajemy oddzielnie
    # category = CharField(max_length=128)
    # photo = CharField(max_length=128)
    # description = TextField(null=True)
    # amount = IntegerField(default=0)
    # price = DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_description(self):
        #pobranie wartości pola description
        initial = self.cleaned_data['description']
        #podział tekstu na części "od kropki do kropki" na zdania
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        #zamina na wielką literę pierwszj litery każdego ze zdań,
        #dodanie kropki, powtórzenie operacji dla kolejnego zdania
        return '.'.join(sentence.capitalize() for sentence in sentences)


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    street = CharField(
        label='Podaj ulicę', widget=Textarea, min_length=3, max_length=128
    )
    home_number = CharField(
        label='Podaj numer domu', widget=Textarea, min_length=1
    )
    flat_number = CharField(
        label='Podaj numer mieszkania', widget=Textarea, min_length=1
    )
    postcode = CharField(
        label='Podaj kod pocztowy', widget=Textarea, min_length=5
    )
    locality = CharField(
        label='Podaj miejscowość zamieszkania', widget=Textarea, min_length=3
    )
    country = CharField(
        label='Podaj kraj zamieszkania', widget=Textarea, min_length=3
    )
    phone_number = CharField(
        label='Podaj numer telefonu', widget=Textarea, min_length=3
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