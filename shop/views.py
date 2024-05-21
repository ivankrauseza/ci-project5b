from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from .models import Product, Media, Transaction
from .forms import AddToBasketForm
from django.db.models import Q
from .logging_utils import log_transaction
import re


def custom_sort_key(media):
    # Extract the base name and the number if present
    match = re.match(r'^(.*?)(?:_(\d+))?(\.\w+)$', media.file.name)
    if match:
        base_name, num, ext = match.groups()
        num = int(num) if num is not None else 0
        return (base_name, num, ext)
    return (media.file.name, 0, '')


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
    return render(request, 'support.html')


def ProductSearch(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(blurb__icontains=query) |
            Q(desc__icontains=query) |
            Q(brand__icontains=query)
        )
    return render(
        request,
        'product-list-search.html',
        {'results': results, 'query': query}
    )


def ProductList(request):
    products = Product.objects.all()

    # Get filter parameters from request
    brand_filter = request.GET.getlist('brand')

    # Apply filters to the queryset if any filter is provided
    if brand_filter:
        products = products.filter(brand__in=brand_filter)

    # Get distinct brands for the filters
    brands = Product.objects.values_list('brand', flat=True).distinct()

    # Create a dictionary to hold the image URLs
    product_images = {}
    for product in products:
        # Query the media file associated with the product ID and SKU
        matching_media = Media.objects.filter(product=product.id, file=f'uploads/{product.sku}.png').first()
        if matching_media:
            product_images[product.id] = matching_media.file.url
        else:
            product_images[product.id] = None  # Set to None if no matching media found

    return render(request, 'product-list.html', {
        'products': products,
        'brands': brands,
        'selected_brands': brand_filter,
        'product_images': product_images,  # Pass the image URLs dictionary to the template
        'MEDIA_URL': settings.MEDIA_URL
    })


def ProductCategories(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'product-list-categories.html')


def ProductDetail(request, sku):
    product = get_object_or_404(Product, sku=sku)
    media_files = Media.objects.filter(product=product)
    # Sort the media files using the custom sort key
    sorted_media_files = sorted(media_files, key=custom_sort_key)

    # Check if the item is in the basket:
    if request.user.is_authenticated:
        product_in_basket = Transaction.objects.filter(
            user=request.user,
            type="B",
            product=product
        ).exists()
    else:
        product_in_basket = False

    # Add the item to the basket:
    if request.method == 'POST':
        form = AddToBasketForm(request.POST, product=product)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            Transaction.objects.create(
                user=request.user,
                product=product,
                quantity=quantity,
                type='B'
            )
            messages.success(request, 'Item added to basket')
            return redirect('product_detail', sku=product.sku)
        else:
            messages.error(request, 'Something went wrong, please try again.')
    else:
        form = AddToBasketForm(product=product)

    return render(request, 'product-detail.html', {
        'form': form,
        'product': product,
        'product_in_basket': product_in_basket,
        'media_files': sorted_media_files,
        })


def Basket(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'basket.html')


def OrderConfirmation(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'order-confirmation.html')


def Dashboard(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'dashboard.html')
