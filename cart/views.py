from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from .forms import CartAddForm
from inventory.models import Product

# Create your views here.


def product_add(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug, quantity__gt=0)
    cart = Cart(request)

    if request.method == "POST":
        form = CartAddForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cart.add(
                product=product,
                quantity=cleaned_data.get("quantity"),
                override_quantity=cleaned_data.get("override"),
            )
    else:
        form = CartAddForm()

    return redirect("cart-detail")


def product_remove(request, product_slug):

    product = get_object_or_404(Product, slug=product_slug, quantity__gt=0)
    cart = Cart(request)
    cart.remove(product=product)
    return redirect("cart-detail")


def cart_detail(request):
    cart = Cart(request)
    
    for item in cart:
        item['update_item_quantity'] = CartAddForm(
            initial={
                'quantity': item['quantity'],
                'override': True,
            }
        )
    context = {'cart': cart}
    return render(request, "cart/cart_detail.html", context)