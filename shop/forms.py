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
        fields = ['name', 'surname', 'street', 'home_number', 'flat_number', 'postcode', 'locality', 'country', 'mail', 'phone_number']

    name = CharField(
        label='Podaj imię', widget=Textarea, min_length=3
    )
    surname = CharField(
        label='Podaj nazwisko', widget=Textarea, min_length=3
    )
    street = CharField(
        label='Podaj ulicę', widget=Textarea, min_length=3
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
    mail = CharField(
        label='Podaj adres e-mail', widget=Textarea, min_length=5
    )
    phone_number = CharField(
        label='Podaj numer telefonu', widget=Textarea, min_length=3
    )

    @atomic
    def save(self, commit=True):
        self.instance.is_activate = False
        result = super().save(commit)
        name = self.cleaned_data['name', 'surname', 'street', 'home_number', 'flat_number', 'postcode', 'locality',
                                 'country', 'mail', 'phone_number']
        profile = Profile(name=name, user=result)
        if commit:
            profile.save()
        return result