from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models.review import Review
from .models.wishlist import Wishlist
from django.views.decorators.http import require_POST
from .models.category import Category
from .models.product import Product
from .models.order import Cart, Order
from .models.userprofile import UserProfile
from .form import RegisterForm, LoginForm
from .models import ShippingAddress
from .form import ShippingAddressForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .models.order import Order
from .models.review import Review
from .models.wishlist import Wishlist
from .models import ShippingAddress
from .models.userprofile import UserProfile

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
                if next_url and request.method == 'GET':
                    return redirect('home') if '/add-to-cart/' in next_url else redirect(next_url)
                return redirect('home')
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
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('search')

    products = Product.objects.all()

    if selected_category:
        products = products.filter(category__id=selected_category)

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'home.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
    })

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models.order import Order
from .models.review import Review
from .models.wishlist import Wishlist
from .models import ShippingAddress
from .models.userprofile import UserProfile



@login_required
def user_dashboard(request):
    # Fetch or create profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(user=request.user)
    wishlist = Wishlist.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    addresses = ShippingAddress.objects.filter(user=request.user)

    return render(request, 'user_dashboard.html', {
        'orders': orders,
        'wishlist': wishlist,
        'reviews': reviews,
        'addresses': addresses,
        'profile': profile,
    })

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
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        return redirect('home')  # Redirect to the product page or home
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('home')  # Redirect to the product page or home
@login_required
def view_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})



@login_required
def download_cart_invoice(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items.exists():
        return HttpResponse("Cart is empty.")

    total = sum(item.total_price() for item in cart_items)

    html = render_to_string('cart_invoice_template.html', {
        'user': request.user,
        'cart_items': cart_items,
        'total': total,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cart_invoice.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating cart invoice.')

    return response

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    
    # Get last verified order (optional safety check for status)
    last_order = Order.objects.filter(user=request.user, is_verified=True).order_by('-created_at').first()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'last_order': last_order
    })


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
    order.generate_invoice_number()

    send_mail(
        'Your ShopMart OTP',
        f'Your OTP for order verification is: {otp}',
        'shopmart@example.com',
        [request.user.email],
        fail_silently=False,
    )

    return redirect('verify_otp', order_id=order.id)


from django.shortcuts import render, redirect, get_object_or_404
from .models import PromoCode
from .models.order import Order, Cart
from .models.ShippingAddress import ShippingAddress
from .form import ShippingAddressForm, PromoCodeForm
from django.core.mail import send_mail
from decimal import Decimal
from django.utils import timezone

@login_required
@login_required
def checkout_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        return redirect('home')

    subtotal = sum(item.total_price() for item in cart_items)
    discount = Decimal('0.00')
    promo_code_applied = None

    if request.method == 'POST' and 'apply_promo' in request.POST:
        promo_form = PromoCodeForm(request.POST)
        if promo_form.is_valid():
            code_entered = promo_form.cleaned_data['code']
            try:
                promo = PromoCode.objects.get(code__iexact=code_entered)
                if promo.is_valid():
                    discount = subtotal * Decimal(promo.discount_percent) / 100
                    promo_code_applied = promo
                    request.session['promo_code'] = promo.code
                else:
                    promo_form.add_error('code', 'Promo code is expired or inactive.')
            except PromoCode.DoesNotExist:
                promo_form.add_error('code', 'Invalid promo code.')
        form = ShippingAddressForm()
        total = subtotal - discount
        return render(request, 'checkout.html', {
            'form': form,
            'promo_form': promo_form,
            'cart_items': cart_items,
            'subtotal': subtotal,
            'discount': discount,
            'total': total,
            'promo_code_applied': promo_code_applied
        })

    elif request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        promo_form = PromoCodeForm()
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.user = request.user
            shipping_address.save()

            promo_code = request.session.get('promo_code')
            if promo_code:
                try:
                    promo = PromoCode.objects.get(code__iexact=promo_code)
                    if promo.is_valid():
                        discount = subtotal * Decimal(promo.discount_percent) / 100
                        promo_code_applied = promo
                except PromoCode.DoesNotExist:
                    pass

            total = subtotal - discount

            order = Order.objects.create(
                user=request.user,
                total=total,
                shipping_address=shipping_address
            )
            order.items.set(cart_items)

            if promo_code_applied:
                order.promo_code = promo_code_applied

            order.generate_invoice_number()
            otp = order.generate_otp()

            send_mail(
                'Your ShopMart OTP',
                f'Your OTP for order verification is: {otp}',
                'shopmart@example.com',
                [request.user.email],
                fail_silently=False,
            )

            request.session.pop('promo_code', None)
            return redirect('verify_otp', order_id=order.id)
    else:
        form = ShippingAddressForm()
        promo_form = PromoCodeForm()

    total = subtotal - discount

    return render(request, 'checkout.html', {
        'form': form,
        'promo_form': promo_form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'promo_code_applied': promo_code_applied
    })


@login_required
def verify_otp(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == order.otp:
            order.is_verified = True
            order.status = 'Confirmed'
            order.save()
            Cart.objects.filter(user=request.user).delete()
            return render(request, 'success.html', {'order_id': order.id})
        else:
            return render(request, 'verify_otp.html', {'order_id': order.id, 'error': 'Invalid OTP'})
    return render(request, 'verify_otp.html', {'order_id': order.id})

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pisa_status = pisa.CreatePDF(html, dest=response)
    return response

def download_invoice(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    template = get_template('invoice_template.html')
    html = template.render({'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.invoice_number or order.id}.pdf"'

    pisa_status = pisa.CreatePDF(BytesIO(html.encode('UTF-8')), dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors while generating the invoice PDF.')
    return response
# views.py
from django.http import StreamingHttpResponse
from time import sleep
from .models import Notification

def sse_notifications(request):
    def event_stream():
        while True:
            offers = "🔥 Flash Sale: 50% OFF!"
            if request.user.is_authenticated:
                Notification.objects.create(user=request.user, title=offers)
            yield f"data: {offers}\n\n"
            sleep(10)
    return StreamingHttpResponse(event_stream(), content_type='text/event-stream')
# store/views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Notification, SpecialOffer

def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk)
    notification.is_active = False  # remove from feed
    notification.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

from django.shortcuts import get_object_or_404, redirect
from .models import SpecialOffer  # Make sure this matches your model name

def mark_offer_read(request, pk):
    offer = get_object_or_404(SpecialOffer, pk=pk)
    offer.is_active = False  # Or set a user-specific "seen" flag if you have one
    offer.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))

