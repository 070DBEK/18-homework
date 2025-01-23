from django import forms
from products.models import Product
from .models import Order, OrderItem
from django.forms.models import inlineformset_factory


class OrderForm(forms.ModelForm):
    # Customizing the 'order_date' field (this will be auto-generated)
    order_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'block text-sm font-medium text-gray-700', 'type': 'date'}),
        label="Date",
        required=False  # This is not needed because it's auto-generated
    )

    # Customizing the 'order_status' field
    order_status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Status"
    )

    # Custom fields for customer details
    customer_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Name"
    )

    customer_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Email"
    )

    customer_phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Phone"
    )

    customer_address = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'block text-sm font-medium text-gray-700', 'rows': 3}),
        label="Address"
    )

    class Meta:
        model = Order
        exclude = ['order_date']


class OrderItemForm(forms.ModelForm):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        widget=forms.Select(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Product"
    )

    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Quantity"
    )

    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Price"
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        return price


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    fields=('product', 'quantity', 'price'),
    extra=1
)
