from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.checkout_step1, name='checkout_step1'),
    path('livraison/', views.checkout_step2, name='checkout_step2'),
    path('paiement/', views.checkout_step3, name='checkout_step3'),
]
