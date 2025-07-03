from django.contrib import admin

from .models.product import Product
from .models.category import Category
from .models.order import Cart, Order
from .models.userprofile import UserProfile


# ---------------- USER PROFILE ADMIN ----------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username', 'phone']


# ---------------- PRODUCT ADMIN ----------------
@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'description')
    search_fields = ('name', 'category__name')


# ---------------- CATEGORY ADMIN ----------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ---------------- CART ADMIN ----------------
@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')


# ---------------- ORDER ADMIN ----------------
@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'is_verified', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('otp', 'created_at')
