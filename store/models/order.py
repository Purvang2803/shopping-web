from django.db import models
from django.contrib.auth.models import User
from .product import Product
from .ShippingAddress import ShippingAddress
from decimal import Decimal
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
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    otp = models.CharField(max_length=6, blank=True)
    is_verified = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_number = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def generate_otp(self):
        """Generate and save a 6-digit OTP"""
        otp_code = str(random.randint(100000, 999999))
        self.otp = otp_code
        self.save()
        return otp_code

    def generate_invoice_number(self):
        """Generate a unique invoice number"""
        if not self.invoice_number:
            # Safe fallback if order not saved yet
            random_part = random.randint(10000, 99999)
            suffix = self.id if self.id else random.randint(1000, 9999)
            self.invoice_number = f"INV-{random_part}-{suffix}"
            self.save()

    def total_with_tax(self):
        """Total amount including 18% tax"""
        return round(self.total * Decimal('1.18'), 2)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
