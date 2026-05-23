from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from products.models import Product
from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get("quantity", 1))

    cart.add(product=product, quantity=quantity)
     # 🔥 Le message de confirmation
    messages.success(request, f"{product.name} ajouté au panier.")
    return redirect("cart:cart_detail")




def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    

    return render(request, "cart/cart_detail.html", {"cart": cart})

from django.contrib import messages

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    product_id_str = str(product.id)
    current_qty = cart.cart.get(product_id_str, {}).get("quantity", 0)

    # 🔥 On vide les anciens messages
    storage = messages.get_messages(request)
    storage.used = True

    if current_qty >= product.stock:
        messages.info(request, f"Stock maximum atteint pour {product.name}.")
        return redirect("cart:cart_detail")

    cart.add(product=product, quantity=1)
    return redirect("cart:cart_detail")






def cart_remove_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=-1)
    return redirect("cart:cart_detail")

import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from .cart import Cart

def create_checkout_session(request):
    cart = Cart(request)

    stripe.api_key = settings.STRIPE_SECRET_KEY

    line_items = []

    for item in cart:
        product = item["product"]
        quantity = item["quantity"]
        price = item["price"]

        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": product.name,
                },
                "unit_amount": int(price * 100),
            },
            "quantity": quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        success_url=request.build_absolute_uri(reverse("cart:success")),
        cancel_url=request.build_absolute_uri(reverse("cart:cart_detail")),
    )

    return redirect(session.url)


def success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, "success.html")

