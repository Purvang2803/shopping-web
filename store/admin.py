from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.order import Cart, Order
from django.contrib import admin
from .models.userprofile import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username', 'phone']


# Product Admin
class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'description')
    search_fields = ('name', 'category__name')


# Cart Admin
class AdminCart(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')


# Order Admin
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'is_verified', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('otp', 'created_at')


# Register Models
admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Cart, AdminCart)
admin.site.register(Order, AdminOrder)
