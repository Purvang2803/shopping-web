from django.urls import path
from .views import (
    register_view, login_view, logout_view, home,
    add_to_cart, view_cart, place_order, verify_otp,checkout_view,download_invoice,add_review,add_to_wishlist,view_wishlist,download_cart_invoice
    , user_dashboard, sse_notifications, mark_notification_read, mark_offer_read
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
    path('download-cart-invoice/', download_cart_invoice, name='download_cart_invoice'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('verify-otp/<int:order_id>/', verify_otp, name='verify_otp'),
     path('add-review/<int:product_id>/', add_review, name='add_review'),
    path('add-to-wishlist/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('notifications/', sse_notifications, name='notifications'),
    path('notification/read/<int:pk>/', mark_notification_read, name='mark_notification_read'),
    path('offer/read/<int:pk>/', mark_offer_read, name='mark_offer_read'),
]
