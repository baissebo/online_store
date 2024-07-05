from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField, BaseInlineFormSet

from catalog.models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                   'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name').lower()
        description = cleaned_data.get('description').lower()

        for word in FORBIDDEN_WORDS:
            if word in name:
                self.add_error('name', f'Слово "{word}" запрещено в названии!')
            if word in description:
                self.add_error('description', f'Слово "{word}" запрещено в описании!')
        return cleaned_data


class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = ("is_published", "description", "category")


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_number', 'version_name', 'is_current')


class BaseVersionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        current_count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data.get('is_current', False):
                current_count += 1
        if current_count > 1:
            raise ValidationError("Можно выбрать только одну версию!")


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    phone = forms.CharField(label='Телефон', max_length=20)
    message = forms.CharField(label='Сообщение', widget=forms.Textarea)
