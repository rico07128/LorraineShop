from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home  # ta page d'accueil

urlpatterns = [
    path("", home, name="home"),  # 👉 ta vraie page d'accueil
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin-fr/", admin.site.urls),
    path("products/", include("products.urls")),  # 👉 produits ici
    path("cart/", include("cart.urls")),  # 👉 panier ici
    path("orders/", include("orders.urls")),  # 👉 commandes ici
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
