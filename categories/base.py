from django import forms
from django.core.exceptions import ValidationError
from django.db import models


def is_alpha_or_space(input_string):
    return all(c.isalpha() or c.isspace() for c in input_string)


class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)


    class Meta:
        abstract = True


class BaseForm(forms.Form):
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
            'placeholder': 'Enter description',
            'rows': 4,
        }),
        label="Description",
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