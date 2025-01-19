from django import forms
from products.models import Product
from .models import Order, OrderItem
from django.forms.models import inlineformset_factory


class OrderForm(forms.ModelForm):
    order_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Date",
        required=False
    )
    order_status = forms.ChoiceField(
        choices=Order.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'block text-sm font-medium text-gray-700'}),
        label="Status"
    )
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


OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)
