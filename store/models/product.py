from django.db import models
from .category import Category
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, default="", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='upload/products/')
    
    # Optional flag to control discount display on homepage
    is_discounted = models.BooleanField(default=True)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def discounted_price(self):
        if self.is_discounted:
            return self.price * Decimal('0.8')  # instead of 0.8 float
        return self.price

    def __str__(self):
        return self.name
