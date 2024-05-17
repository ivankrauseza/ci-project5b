from django.shortcuts import render
from django.contrib import messages


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
    # messages.info(request, 'Test Toast')
    return render(request, 'product-list.html')


def ProductCategories(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'product-list-categories.html')


def ProductDetail(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'product-detail.html')


def Basket(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'basket.html')


def OrderConfirmation(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'order-confirmation.html')


def Dashboard(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'dashboard.html')
