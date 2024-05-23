from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
import uuid
from django.conf import settings
from django.contrib import messages
from .models import Product, Media, Transaction, Contact, Support, SalesOrder, SalesOrderItem, Profile
from .forms import AddToBasketForm, BasketQuantityForm, ContactForm, SupportForm,  BillingForm, ShippingForm
from django.db.models import Q
from .logging_utils import log_transaction
import re
# Basket
from django.core import exceptions
from decimal import Decimal
from django.utils import timezone

# Email
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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


# EMAIL - Send Order Confirmation
def send_order_email(sender_email, sender_password, to_email, subject, body, content_type='plain'):
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, content_type))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


# EMAIL - Send Contact Form
def send_email(subject, body, to_email):
    sender_email = os.environ.get('EMAIL_SEND')
    sender_password = os.environ.get('EMAIL_KEY')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


# EMAIL - Send Support Form
def support_email(subject, body, to_email):
    sender_email = os.environ.get('EMAIL_SEND')
    sender_password = os.environ.get('EMAIL_KEY')

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message.as_string())
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")


def ContactPage(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.reference_number = str(uuid.uuid4())[:8]  # Generate a unique reference number
            contact.save()

            # Prepare user email
            user_subject = "Contact Form Submission"
            user_body = (f"Dear {contact.name},\n\nThank you for contacting us. "
                         f"Your message has been received.\n\nMessage:\n{contact.message}\n\n"
                         f"Reference Number: {contact.reference_number}\n\nBest Regards,\nYour Team")
            
            # Send confirmation email to the user
            send_email(user_subject, user_body, contact.email)

            # Prepare admin email
            admin_subject = "New Contact Form Submission"
            admin_body = (f"A new contact form submission has been received.\n\n"
                          f"Name: {contact.name}\nEmail: {contact.email}\n"
                          f"Message:\n{contact.message}\n\n"
                          f"Reference Number: {contact.reference_number}")
            admin_email = os.environ.get('EMAIL_ADMIN')

            # Send notification email to the admin
            send_email(admin_subject, admin_body, admin_email)

            messages.success(request, 'Your message has been sent!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def PrivacyPage(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'privacy.html')


def CookiePage(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'cookie.html')


def SupportPage(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.reference_number = str(uuid.uuid4())[:8]  # Generate a unique reference number
            contact.save()

            # Prepare user email
            user_subject = "Contact Form Submission"
            user_body = (f"Dear {contact.name},\n\nThank you for contacting us. "
                         f"Your message has been received.\n\nMessage:\n{contact.message}\n\n"
                         f"Reference Number: {contact.reference_number}\n\nBest Regards,\nYour Team")

            # Send confirmation email to the user
            send_email(user_subject, user_body, contact.email)

            # Prepare admin email
            admin_subject = "New Contact Form Submission"
            admin_body = (f"A new contact form submission has been received.\n\n"
                          f"Name: {contact.name}\nEmail: {contact.email}\n"
                          f"Message:\n{contact.message}\n\n"
                          f"Reference Number: {contact.reference_number}")
            admin_email = os.environ.get('EMAIL_ADMIN')

            # Send notification email to the admin
            send_email(admin_subject, admin_body, admin_email)

            messages.success(request, 'Your message has been sent!')
            return redirect('support')
    else:
        form = ContactForm()
    return render(request, 'support.html', {'form': form})


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
    order_by = request.GET.get('order_by')

    # Apply filters to the queryset if any filter is provided
    if brand_filter:
        products = products.filter(brand__in=brand_filter)

    # Apply sorting to the queryset if order_by is provided
    if order_by == 'asc':
        products = products.order_by('price')
    elif order_by == 'desc':
        products = products.order_by('-price')

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
        'MEDIA_URL': settings.MEDIA_URL,
        'order_by': order_by
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


@login_required
def Basket(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = None

    if user.is_authenticated and profile:
        billing_fields = [
            profile.billing_name,
            profile.billing_address,
            profile.billing_code,
            profile.billing_phone,
        ]
        shipping_fields = [
            profile.shipping_name,
            profile.shipping_address,
            profile.shipping_code,
            profile.shipping_phone,
        ]

        all_billing_filled = all(billing_fields)
        all_shipping_filled = all(shipping_fields)

        can_pay = all_billing_filled and all_shipping_filled
    else:
        can_pay = False

    user_transactions = Transaction.objects.filter(user=request.user, type='B')

    for transaction in user_transactions:
        transaction.subtotal = transaction.quantity * transaction.product.price

    total_basket_value = sum(transaction.subtotal for transaction in user_transactions)
    delivery_amount = Decimal('10.00')
    vat_rate = Decimal('0.23')
    vat_amount = total_basket_value * vat_rate
    total_amount = total_basket_value + delivery_amount + vat_amount

    if request.method == "POST":
        if request.POST.get('action') == 'create_order':
            sales_order = SalesOrder.objects.create(
                user=user,
                number=f"SO{timezone.now().strftime('%Y%m%d%H%M%S')}",
                billing_name=profile.billing_name,
                billing_address=profile.billing_address,
                billing_phone=profile.billing_phone,
                shipping_name=profile.shipping_name,
                shipping_address=profile.shipping_address,
                shipping_phone=profile.shipping_phone,
                items_total=total_basket_value,
                delivery_amount=delivery_amount,
                vat_amount=vat_amount,
                order_total=total_amount,
            )

            for transaction in user_transactions:
                SalesOrderItem.objects.create(
                    sales_order=sales_order,
                    product=transaction.product,
                    quantity=transaction.quantity,
                    price=transaction.product.price
                )
                transaction.product.stock -= transaction.quantity
                transaction.product.save()

            user_transactions.delete()

            # Sending emails to customer and store owners
            sender_email = os.environ.get('EMAIL_SEND')
            sender_password = os.environ.get('EMAIL_KEY')

            # Customer Email
            customer_subject = 'Order Confirmation'
            customer_body = f"""
            <html>
            <body>
                <h2>Thank you for your order!</h2>
                <p><strong>Order Number:</strong> {sales_order.number}</p>
                <p><strong>Billing Name:</strong> {sales_order.billing_name}</p>
                <p><strong>Billing Address:</strong> {sales_order.billing_address}</p>
                <p><strong>Shipping Name:</strong> {sales_order.shipping_name}</p>
                <p><strong>Shipping Address:</strong> {sales_order.shipping_address}</p>
                <p><strong>Total Amount:</strong> €{sales_order.order_total}</p>
                <p>We will notify you once your order is shipped.</p>
            </body>
            </html>
            """

            send_order_email(
                sender_email,
                sender_password,
                user.email,
                customer_subject,
                customer_body,
                'html'
            )

            # Webstore Team Email
            store_team_email = 'ivankrause85@gmail.com'
            store_subject = 'New Order Received'
            store_body = f"""
            <html>
            <body>
                <h2>New Order Received</h2>
                <p><strong>Order Number:</strong> {sales_order.number}</p>
                <p><strong>Customer:</strong> {user.get_full_name()}</p>
                <p><strong>Billing Name:</strong> {sales_order.billing_name}</p>
                <p><strong>Billing Address:</strong> {sales_order.billing_address}</p>
                <p><strong>Shipping Name:</strong> {sales_order.shipping_name}</p>
                <p><strong>Shipping Address:</strong> {sales_order.shipping_address}</p>
                <p><strong>Total Amount:</strong> €{sales_order.order_total}</p>
                <p>Please process the order promptly.</p>
            </body>
            </html>
            """

            send_order_email(
                sender_email,
                sender_password,
                store_team_email,
                store_subject,
                store_body,
                'html'
            )

            return redirect('confirm', order_id=sales_order.id)

        elif request.POST.get('form_type') == 'billing':
            billing_form = BillingForm(request.POST, instance=profile)
            if billing_form.is_valid():
                billing_form.save()
                return redirect('basket')
        elif request.POST.get('form_type') == 'shipping':
            shipping_form = ShippingForm(request.POST, instance=profile)
            if shipping_form.is_valid():
                shipping_form.save()
                return redirect('basket')

    billing_form = BillingForm(instance=profile)
    shipping_form = ShippingForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'user_transactions': user_transactions,
        'total_basket_value': total_basket_value,
        'delivery_amount': delivery_amount,
        'vat_amount': vat_amount,
        'total_amount': total_amount,
        'billing_form': billing_form,
        'shipping_form': shipping_form,
        'can_pay': can_pay,
    }
    return render(request, 'basket.html', context)


# EDIT BASKET LINES:
@login_required
def basket_quantity_update(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if request.method == 'POST':
        form = BasketQuantityForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
        messages.info(request, 'Quantity Updated')
        return redirect('basket')
    else:
        form = BasketQuantityForm(instance=transaction)
    return render(request, 'basket_update.html', {'form': form})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if transaction.user == request.user:
        transaction.delete()
        messages.info(request, 'Item Removed')
    return redirect('basket')


def OrderConfirmation(request, order_id):
    order = SalesOrder.objects.get(id=order_id, user=request.user)
    return render(request, 'order-confirmation.html', {'order': order})


@login_required
def profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    billing_form = BillingForm(instance=profile)
    shipping_form = ShippingForm(instance=profile)

    context = {
        'user': user,
        'billing_form': billing_form,
        'shipping_form': shipping_form,
    }
    return render(request, 'profile.html', context)


@login_required
def update_billing(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        billing_form = BillingForm(request.POST, instance=profile)
        if billing_form.is_valid():
            billing_form.save()
            return redirect('profile')

    billing_form = BillingForm(instance=profile)
    shipping_form = ShippingForm(instance=profile)

    context = {
        'user': user,
        'billing_form': billing_form,
        'shipping_form': shipping_form,
    }
    return render(request, 'profile.html', context)


@login_required
def update_shipping(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        shipping_form = ShippingForm(request.POST, instance=profile)
        if shipping_form.is_valid():
            shipping_form.save()
            return redirect('profile')

    billing_form = BillingForm(instance=profile)
    shipping_form = ShippingForm(instance=profile)

    context = {
        'user': user,
        'billing_form': billing_form,
        'shipping_form': shipping_form,
    }
    return render(request, 'profile.html', context)


@login_required
def orders(request):
    user_orders = SalesOrder.objects.filter(user=request.user)
    context = {
        'user_orders': user_orders,
    }
    return render(request, 'orders.html', context)


def Dashboard(request):
    # messages.info(request, 'Test Toast')
    return render(request, 'dashboard.html')
