from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    orders = request.user.order_set.all()

    return render(request, "account/profile.html", {
        "profile": profile,
        "orders": orders,
    })


@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Mise à jour User
        request.user.first_name = request.POST.get("first_name")
        request.user.last_name = request.POST.get("last_name")
        request.user.email = request.POST.get("email")
        request.user.save()

        # Mise à jour UserProfile
        profile.address = request.POST.get("address")
        profile.postal_code = request.POST.get("postal_code")
        profile.city = request.POST.get("city")
        profile.region = request.POST.get("region")
        profile.phone = request.POST.get("phone")
        profile.save()

        return redirect("profil")

    return render(request, "account/edit_profile.html", {
        "profile": profile
    })
