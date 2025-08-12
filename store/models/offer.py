from django.db import models

class SpecialOffer(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)  # ✅ add this
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

