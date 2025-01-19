from django import forms
from django.core.exceptions import ValidationError
from .base import BaseForm


class CategoryForm(BaseForm):
    desc = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'placeholder': 'Enter category description',
            'rows': 4,
        }),
        label="Description",
    )

    icon = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'accept': 'image/*',
        }),
        label="Category image",
        required=False
    )

    def clean_icon(self):
        icon_url = self.cleaned_data.get('icon')
        if not icon_url:
            raise ValidationError('This field is required.')
        return icon_url

