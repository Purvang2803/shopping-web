from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200,default="",blank=True,null=True)
    price = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=1)
    image = models.ImageField(upload_to='upload/products/')


    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def __str__(self):
        return self.name