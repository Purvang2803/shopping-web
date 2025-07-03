from django.urls import path
from .views import (
    register_view, login_view, logout_view, home,
    add_to_cart, view_cart, place_order, verify_otp,checkout_view,download_invoice,add_review,add_to_wishlist,view_wishlist
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('place-order/', place_order, name='place_order'),
    path('checkout/',checkout_view, name='checkout'),
    path('invoice/download/<int:order_id>/',download_invoice, name='download_invoice'),
    path('verify-otp/<int:order_id>/', verify_otp, name='verify_otp'),
     path('add-review/<int:product_id>/', add_review, name='add_review'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
]
