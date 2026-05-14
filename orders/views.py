from django.shortcuts import render
from .models import Order, OrderItem
from cart.cart import Cart

def order_create(request):
    cart = Cart(request)

    if request.method == "POST":
        order = Order.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"],
            address=request.POST["address"],
            postal_code=request.POST["postal_code"],
            city=request.POST["city"],
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                price=item["product"].price,
                quantity=item["quantity"],
            )

        cart.clear()

        return render(request, "orders/created.html", {"order": order})

    return render(request, "orders/create.html", {"cart": cart})
    