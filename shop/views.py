from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Product


def Home(request):
    messages.info(request, 'Test Toast')
    return render(request, 'index.html')


def About(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'about.html')


def Contact(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'contact.html')


def Privacy(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'privacy.html')


def Support(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'support.html')


def ProductSearch(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'product-list-search.html')


def ProductList(request):
    products = Product.objects.all()
    return render(request, 'product-list.html', {'products': products})


def ProductCategories(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'product-list-categories.html')


def ProductDetail(request, sku):
    product = get_object_or_404(Product, sku=sku)
    return render(request, 'product-detail.html', {'product': product})


def Basket(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'basket.html')


def OrderConfirmation(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'order-confirmation.html')


def Dashboard(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'dashboard.html')
