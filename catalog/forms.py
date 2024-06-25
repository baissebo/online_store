from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from catalog.models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                   'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name').lower()
        description = cleaned_data.get('description').lower()

        for word in FORBIDDEN_WORDS:
            if word in name or word in description:
                raise forms.ValidationError(f'Слово "{word}" запрещено')

        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_number', 'version_name', 'is_current')

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get('is_current')
        instance = self.instance

        if is_current:
            current_versions = Version.objects.filter(
                product=instance.product,
                is_current=True
            ).exclude(pk=instance.pk)
            if current_versions.exists():
                raise ValidationError("Можно выбрать только одну активную версию продукта!")

        return cleaned_data

    def save(self, commit=True):
        version = super().save(commit=False)

        if version.is_current:
            Version.objects.filter(
                product=version.product,
                is_current=True
            ).exclude(pk=version.pk).update(is_current=False)

        return super().save(commit=commit)


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)
