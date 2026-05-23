from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from . import views

from LorraineShop.views import home
from accounts.views import profile, edit_profile

urlpatterns = [
    # Changement de langue
    path("i18n/", include("django.conf.urls.i18n")),
    
]

urlpatterns += i18n_patterns(

    # Page d'accueil
    path("", home, name="home"),

    # Comptes
    path("accounts/", include("allauth.urls")),
    path("mon-compte/", profile, name="profil"),
    path("mon-compte/modifier/", edit_profile, name="edit_profile"),

    # Déconnexion
    path("logout/", include("django.contrib.auth.urls")),

    # Admin
    path("admin-fr/", admin.site.urls),

    # Apps
    path("products/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
