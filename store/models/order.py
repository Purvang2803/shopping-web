from django.db import models
from django.contrib.auth.models import User
from .product import Product
from .ShippingAddress import ShippingAddress
import random

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    total = models.FloatField()
    otp = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ Added field
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_otp(self):
        otp_code = str(random.randint(100000, 999999))
        self.otp = otp_code
        self.save()
        return otp_code

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
