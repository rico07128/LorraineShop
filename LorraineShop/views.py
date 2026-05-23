from django.shortcuts import redirect, render


def home(request):
    return render(request, "home.html")

def checkout_step1(request):
    if request.method == "POST":
        # tu peux stocker les infos dans la session si tu veux
        request.session['checkout'] = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'address': request.POST.get('address'),
            'postal_code': request.POST.get('postal_code'),
            'city': request.POST.get('city'),
        }
        return redirect('checkout_step2')

    return render(request, 'checkout/step1.html')


def checkout_step2(request):
    if request.method == "POST":
        request.session['checkout']['shipping'] = request.POST.get('shipping')
        return redirect('checkout_step3')

    return render(request, 'checkout/step2.html')


def checkout_step3(request):
    if request.method == "POST":
        # ici tu finalises la commande
        return redirect('/merci/')  # ou page de confirmation

    return render(request, 'checkout/step3.html')
