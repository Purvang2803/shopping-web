from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.order import Cart, Order
from .models.userprofile import UserProfile
from .models import PromoCode
from .models import SpecialOffer
from .models import Notification

# ---------------- Custom Price Range Filter ----------------
class FlipkartStylePriceFilter(admin.SimpleListFilter):
    title = 'Price Range'
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return [
            ('<1k', 'Below ₹1,000'),
            ('1k-10k', '₹1,000 – ₹10,000'),
            ('10k-50k', '₹10,000 – ₹50,000'),
            ('50k-1L', '₹50,000 – ₹1,00,000'),
            ('>1L', 'Above ₹1,00,000'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == '<1k':
            return queryset.filter(price__lt=1000)
        elif value == '1k-10k':
            return queryset.filter(price__gte=1000, price__lt=10000)
        elif value == '10k-50k':
            return queryset.filter(price__gte=10000, price__lt=50000)
        elif value == '50k-1L':
            return queryset.filter(price__gte=50000, price__lt=100000)
        elif value == '>1L':
            return queryset.filter(price__gte=100000)
        return queryset


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
    list_filter = ['category', FlipkartStylePriceFilter]  # 👈 Price range filter added


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


# ---------------- PROMOCODE ADMIN ----------------
@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'valid_from', 'valid_to', 'active']
    list_filter = ['active', 'valid_from', 'valid_to']
    search_fields = ['code']


# ---------------- ORDER ADMIN ----------------
@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'is_verified', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('otp', 'created_at')



@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'discount_percent', 'created_at')

# store/admin.py

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'created_at', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'message')



