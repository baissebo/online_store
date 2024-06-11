from django import forms
from catalog.models import Product


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)
