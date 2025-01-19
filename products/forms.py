from django import forms
from django.core.exceptions import ValidationError
from .models import Category


def is_alpha_or_space(input_string):
    return all(c.isalpha() or c.isspace() for c in input_string)


class ProductForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'placeholder': 'Enter name',
        }),
        label="Name",
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={
            'class': 'block text-sm font-medium text-gray-700',
        }),
        label="Category",
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'placeholder': 'Enter product price',
        }),
        label="Price",
    )
    desc = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'placeholder': 'Enter product description',
            'rows': 4,
        }),
        label="Description",
    )
    img = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'accept': 'image/*',
        }),
        label="Product image",
    )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not is_alpha_or_space(name):
            raise ValidationError('Name must contain only letters!')
        return name

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if category is None:
            raise forms.ValidationError("You must select a valid category.")
        return category

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Price must be a positive number.")
        return price

    def clean_desc(self):
        desc = self.cleaned_data.get('desc')
        if len(desc) < 10:
            raise ValidationError('Description must be at least 10 characters')
        return desc

    def clean_img(self):
        img_url = self.cleaned_data.get('img')
        if not img_url:
            raise ValidationError('This field is required.')
        return img_url