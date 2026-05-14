from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price)
            }
        self.cart[product_id]["quantity"] += quantity

         # 👉 C’est ICI qu’on ajoute le contrôle du stock
        if self.cart[product_id]["quantity"] > product.stock:
         self.cart[product_id]["quantity"] = product.stock
        self.save()

    def save(self):
        # 🔥 C’est CE QUI MANQUAIT
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        for product_id, item in self.cart.items():
            product = Product.objects.get(id=product_id)
            yield {
                "product": product,
                "quantity": item["quantity"],
                "price": Decimal(item["price"]),
                "total_price": Decimal(item["price"]) * item["quantity"],
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
        Decimal(item["price"]) * item["quantity"]
        for item in self.cart.values()
    )
    def clear(self):
        # Supprime le panier de la session
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True
