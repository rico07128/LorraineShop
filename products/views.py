from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, "products/product_list.html", {
        "category": category,
        "categories": categories,
        "products": products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, "products/product_detail.html", {
        "product": product
    })
