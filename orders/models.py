from django.db import models
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order_id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super(OrderItem, self).save(*args, **kwargs)

    def total(self):
        if self.quantity and self.price:
            return self.quantity * self.price
        return 0

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"