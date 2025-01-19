from django import forms
from django.core.exceptions import ValidationError
from .models import Category
from categories.base import BaseForm


class ProductForm(BaseForm):
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

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise ValidationError("Stock cannot be negative.")
        return stock
