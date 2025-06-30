from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User

from django.views.decorators.http import require_POST

from .models.product import Product
from .models.order import Cart, Order
from .models.userprofile import UserProfile
from .form import RegisterForm, LoginForm  # ✅ Make sure this is correctly named
from .models import ShippingAddress
from .form import ShippingAddressForm


# ---------------- AUTH ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, phone=form.cleaned_data['phone'])
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('home')
            else:
                return render(request, 'auth/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')


# ---------------- HOME ----------------
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# ---------------- CART ----------------



@require_POST
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('view_cart')




@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


# ---------------- ORDER ----------------
@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')

    total = sum(item.total_price() for item in cart_items)
    order = Order.objects.create(user=request.user, total=total)
    order.items.set(cart_items)
    otp = order.generate_otp()

    send_mail(
        'Your ShopMart OTP',
        f'Your OTP for order verification is: {otp}',
        'shopmart@example.com',
        [request.user.email],
        fail_silently=False,
    )

    return redirect('verify_otp', order_id=order.id)

@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()

            # Place Order
            total = sum(item.total_price() for item in cart_items)
            order = Order.objects.create(user=request.user, total=total)
            order.items.set(cart_items)
            order.shipping_address = shipping_address  # ✅ Ensure your Order model has this FK
            otp = order.generate_otp()

            send_mail(
                'Your ShopMart OTP',
                f'Your OTP for order verification is: {otp}',
                'shopmart@example.com',
                [request.user.email],
                fail_silently=False,
            )

            return redirect('verify_otp', order_id=order.id)
    else:
        form = ShippingAddressForm()

    return render(request, 'checkout.html', {'form': form, 'cart_items': cart_items})


@login_required
def verify_otp(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == order.otp:
            order.is_verified = True
            order.save()
            Cart.objects.filter(user=request.user).delete()
            return render(request, 'success.html')
        else:
            return render(request, 'verify_otp.html', {'order_id': order.id, 'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html', {'order_id': order.id})
