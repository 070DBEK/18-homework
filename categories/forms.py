from django import forms
from django.core.exceptions import ValidationError


def is_alpha_or_space(input_string):
    return all(c.isalpha() or c.isspace() for c in input_string)


class CategoryForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'block text-sm font-medium text-gray-700',
            'placeholder': 'Enter name',
        }),
        label="Name",
    )

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

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not is_alpha_or_space(name):
            raise ValidationError('Name must contain only letters!')
        return name

    def clean_desc(self):
        desc = self.cleaned_data.get('desc')
        if len(desc) < 10:
            raise ValidationError('Description must be at least 10 characters')
        return desc

    def clean_icon(self):
        icon_url = self.cleaned_data.get('icon')
        if not icon_url:
            raise ValidationError('This field is required.')
        return icon_url


