from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URLs i18n (obligatoire pour setlang)
    path("i18n/", include("django.conf.urls.i18n")),
    # Admin normal (le middleware forcera la langue)
    path("admin-fr/", admin.site.urls),
    # Tes apps
    path("", include("products.urls")),
    path("", include("cart.urls")),
    path("", include("orders.urls")),
]

# Fichiers statiques & médias
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
