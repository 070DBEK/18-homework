from django.db import models
from categories.models import Category
from categories.base import BaseModel


class Product(BaseModel):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name
