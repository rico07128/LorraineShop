from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("", views.cart_detail, name="cart_detail"),

    # 👉 On change l’URL pour éviter le conflit
    path("add_one/<int:product_id>/", views.cart_add, name="cart_add"),

    path("remove_one/<int:product_id>/", views.cart_remove_one, name="cart_remove_one"),
    path("checkout/", views.create_checkout_session, name="checkout"),
    path("success/", views.success, name="success"),

]
