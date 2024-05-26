from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from shop.models import Product, Media, SalesOrder
from .forms import ProductForm, MediaForm, SalesOrderStatusForm
from django.contrib import messages


@login_required
def erp(request):
    return render(request, 'erp.html')


@login_required
def erp_products(request):
    products = Product.objects.all()
    return render(request, 'erp-products.html', {'products': products})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Product created successfully.')
            # Redirect to the edit view with the pk of the created product
            return redirect('erp_product_edit', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'erp-product-create.html', {'form': form})


class product_edit(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        product_form = ProductForm(instance=product)
        media_form = MediaForm()
        return render(request, 'erp-product-edit.html', {'product_form': product_form, 'media_form': media_form, 'product': product})

    def post(self, request, pk):
        product = Product.objects.get(pk=pk)
        product_form = ProductForm(request.POST, instance=product)
        media_form = MediaForm(request.POST, request.FILES)
        # Handling product form submission
        if 'product_submit' in request.POST:
            if product_form.is_valid():
                product = product_form.save()
                return redirect('erp_products')
            
        # Handling media form submission
        elif 'media_submit' in request.POST:
            if media_form.is_valid():
                media = media_form.save(commit=False)
                media.product = product
                media.save()
                return redirect('erp_product_edit', pk=product.pk)  # Change this to your actual product list view name
        return render(request, 'erp-product-edit.html', {'product_form': product_form, 'media_form': media_form})
    

class product_media_delete(View):
    def post(self, request, pk):
        media = get_object_or_404(Media, pk=pk)
        product = media.product
        media.delete()
        return redirect('erp_product_edit', pk=product.pk)

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('erp_products')
    return render(request, 'erp-product-delete.html', {'product': product})


@login_required
def erp_orders(request):
    orders = SalesOrder.objects.all().order_by('-date')
    return render(request, 'erp-orders.html', {'orders': orders})


@login_required
def erp_order_detail(request, order_number):
    sales_order = get_object_or_404(SalesOrder, number=order_number)
    sales_order_items = sales_order.items.all()

    if request.method == 'POST':
        form = SalesOrderStatusForm(request.POST, instance=sales_order)
        if form.is_valid():
            form.save()
            return redirect('erp_order_detail', order_number=order_number)
    else:
        form = SalesOrderStatusForm(instance=sales_order)

    context = {
        'sales_order': sales_order,
        'sales_order_items': sales_order_items,
        'form': form,
    }
    return render(request, 'erp-order-detail.html', context)
