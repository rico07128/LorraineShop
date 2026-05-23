from django.shortcuts import render, redirect
from cart.cart import Cart
from decimal import Decimal

def checkout_step1(request):
    cart = Cart(request)
    subtotal = cart.get_total_price()
    shipping_price = Decimal("0")
    total = subtotal

    # Préremplissage
    if request.user.is_authenticated:
        user = request.user

        # Récupération du UserProfile
        profile = getattr(user, "userprofile", None)

        initial_data = {
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "email": user.email or "",
            "address": profile.address if profile else "",
            "postal_code": profile.postal_code if profile else "",
            "city": profile.city if profile else "",
        }
    else:
        initial_data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "address": "",
            "postal_code": "",
            "city": "",
        }

    if request.method == "POST":
        request.session['checkout'] = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'postal_code': request.POST.get('postal_code'),
            'city': request.POST.get('city'),
            'shipping_price': 0,
            'shipping': None,
        }
        request.session.modified = True
        return redirect('checkout_step2')

    return render(request, 'checkout/step1.html', {
        "cart": cart,
        "subtotal": subtotal,
        "shipping_price": shipping_price,
        "total": total,
        "initial": initial_data,
    })




def checkout_step2(request):
    cart = Cart(request)
    subtotal = cart.get_total_price()

    # On garantit que checkout existe
    if 'checkout' not in request.session:
        request.session['checkout'] = {}

    # Valeur par défaut
    shipping_price = Decimal(request.session['checkout'].get('shipping_price', 0))

    if request.method == "POST":
        shipping_method = request.POST.get('shipping')

        shipping_prices = {
            "standard": Decimal("4.90"),
            "express": Decimal("9.90"),
            "pickup": Decimal("3.50"),
        }

        shipping_price = shipping_prices.get(shipping_method, Decimal("0"))

        request.session['checkout']['shipping'] = shipping_method
        request.session['checkout']['shipping_price'] = float(shipping_price)
        request.session.modified = True

        return redirect('checkout_step3')

    total = subtotal + shipping_price

    return render(request, 'checkout/step2.html', {
        "cart": cart,
        "subtotal": subtotal,
        "shipping_price": shipping_price,
        "total": total,
    })


def checkout_step3(request):
    cart = Cart(request)
    subtotal = cart.get_total_price()

    checkout = request.session.get('checkout', {})

    shipping_price = Decimal(checkout.get('shipping_price', 0))
    shipping_method = checkout.get("shipping", "")

    total = subtotal + shipping_price

    # Infos client
    customer = {
        "first_name": checkout.get("first_name", ""),
        "last_name": checkout.get("last_name", ""),
        "address": checkout.get("address", ""),
        "postal_code": checkout.get("postal_code", ""),
        "city": checkout.get("city", ""),
    }

    # Traduction du mode de livraison
    shipping_labels = {
        "standard": "Livraison Standard (3–5 jours)",
        "express": "Livraison Express (24h)",
        "pickup": "Point Relais",
    }

    shipping_label = shipping_labels.get(shipping_method, "—")

    if request.method == "POST":
        return redirect('/merci/')

    return render(request, 'checkout/step3.html', {
        "cart": cart,
        "subtotal": subtotal,
        "shipping_price": shipping_price,
        "shipping_label": shipping_label,
        "total": total,
        "customer": customer,
    })
