from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Cart, CartItem
from apps.product.models import Product

# Create your views here.


def _ensure_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key

def _get_or_create_cart(request):
    session_key = _ensure_session(request)

    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
        return cart



def cart_detail(request):
    cart = _get_or_create_cart(request)
    items = cart.items.all()
    total = cart.get_total_price_for_all_items()

    return render(request, 'cart.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, pk=product_id)

    cart = _get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    messages.success(request, f'{product.name} додано у корзину.')
    return redirect('cart:detail')


@require_POST
def update_cart_item(request, item_id):
    action = request.POST.get('action')
    item = get_object_or_404(CartItem, pk=item_id)
    cart = _get_or_create_cart(request)

    if item.cart != cart:
        messages.error(request, "Немає доступу до цього товару.")
        return redirect('cart:detail')

    if action == 'remove':
        item.delete()
        messages.success(request, "Товар видалено з корзини.")
    else:
        qty = int(request.POST.get('quantity', 1))
        if qty <= 0:
            item.delete()
        else:
            item.quantity = qty
            item.save()
        messages.success(request, "Кількість оновлено.")
    return redirect('cart:detail')

