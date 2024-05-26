import os
import time
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from decimal import Decimal

from allauth.account.signals import user_signed_up
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.text import slugify
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


@receiver(user_signed_up)
def create_user_profile(sender, user, **kwargs):
    try:
        customer = stripe.Customer.create(email=user.email)
        Profile.objects.get_or_create(
            user=user,
            defaults={'stripe_id': customer.id}
        )
    except Exception as e:
        # Log the error or print it to the console for debugging
        print(f"Error creating Stripe customer: {e}")


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception as e:
            # Log the error or print it to the console for debugging
            print(f"Error creating profile: {e}")
    else:
        try:
            instance.profile.save()
        except Exception as e:
            # Log the error or print it to the console for debugging
            print(f"Error saving profile: {e}")


@receiver(user_logged_in)
def check_and_create_stripe_customer(sender, request, user, **kwargs):
    try:
        profile = user.profile
        if not profile.stripe_id:
            # Create a new Stripe Customer
            customer = stripe.Customer.create(
                email=user.email  # Assuming email is a unique identifier in Stripe
            )
            profile.stripe_id = customer.id
            profile.save()
        print("User logged in signal triggered")
    except Profile.DoesNotExist as e:
        # Handle the case where a profile doesn't exist
        print(f"Error saving profile: {e}")
        pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=50, blank=True, null=True)
    billing_name = models.CharField(max_length=255)
    billing_address = models.TextField()
    billing_code = models.CharField(max_length=20, blank=True)
    billing_phone = models.CharField(max_length=20, blank=True)
    shipping_name = models.CharField(max_length=255, blank=True)
    shipping_address = models.TextField(blank=True)
    shipping_code = models.CharField(max_length=20, blank=True)
    shipping_phone = models.CharField(max_length=20, blank=True)


# Error if value is less than 0 :
def validate_non_negative(value):
    if value < 0:
        raise ValidationError(f'{value} cannot be less than 0.00.')


# Product model :
class Product(models.Model):
    sku = models.CharField(max_length=255, default='', unique=True)
    name = models.CharField(max_length=255, default='', null=False)
    blurb = models.TextField(default='', blank=True)
    desc = models.TextField(default='', blank=True)
    stock = models.IntegerField(default=0, validators=[validate_non_negative])
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default='0.00',
        validators=[validate_non_negative]
    )
    brand = models.CharField(max_length=255, default='Cadence')
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    blocked = models.BooleanField(default=False)
    
    collection_choices = [
        ('HANDTOOLS', 'Hand Tools'),
        ('POWERTOOLS', 'Power Tools'),
        ('TESTING', 'Testing Equipment'),
        ('CONSUMABLES', 'Consumables'),
        ('STORAGE', 'Storage'),
        ('WEARABLE', 'Wearables'),
    ]
    collection = models.CharField(
        max_length=20,
        choices=collection_choices,
        default='HANDTOOLS',
    )
    
    type_choices = [
        ('PHYSICAL', 'Physical'),
        ('DIGITAL', 'Digital'),
        ('SUBSCRIPTION', 'Subscription'),
        ('LABOUR', 'Labour'),
    ]
    type = models.CharField(
        max_length=20,
        choices=type_choices,
        default='PHYSICAL',
    )

    def get_collection_slug(self):
        return slugify(dict(self.collection_choices).get(self.collection, ''))

    def clean(self):
        super().clean()
        if self.price < 0:
            raise ValidationError({'price': 'Price cannot be negative.'})
        if self.stock < 0:
            raise ValidationError({'stock': 'Stock cannot be negative.'})

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Media(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    file = models.ImageField(upload_to='uploads/', null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    version = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.file:
            # Open the image
            img = Image.open(self.file)

            # Resize the image if it exceeds 1024px x 1024px
            max_size = (1024, 1024)
            if img.width > max_size[0] or img.height > max_size[1]:
                img.thumbnail(max_size, Image.BICUBIC)

                # Center the image on a 1024px x 1024px canvas
                new_img = Image.new("RGB", max_size, (255, 255, 255))  # White background
                position = ((max_size[0] - img.width) // 2, (max_size[1] - img.height) // 2)
                new_img.paste(img, position)

                # Save the resized image to a BytesIO buffer
                img_io = BytesIO()
                img.save(img_io, format='JPEG')

                # Save the resized image
                img_io = BytesIO()
                new_img.save(img_io, format='JPEG')
                self.file.save(
                    os.path.splitext(self.file.name)[0] + ".jpg",
                    ContentFile(img_io.getvalue()),
                    save=False
                )

                # Create thumbnail version
                thumbnail_size = (256, 256)
                img.thumbnail(thumbnail_size, Image.BICUBIC)  # Resize with anti-aliasing for thumbnail
                thumbnail_io = BytesIO()
                img.save(thumbnail_io, format='JPEG')
                self.thumbnail.save(
                    os.path.splitext(self.file.name)[0] + ".jpg",
                    ContentFile(thumbnail_io.getvalue()),
                    save=False
                )

        # Check if a file with the same name exists
        existing_media = Media.objects.filter(
            product=self.product,
            file__contains=os.path.basename(self.file.name)
        ).order_by('-date_added').first()

        if existing_media:
            # Increment the version number
            self.version = existing_media.version + 1

            # Generate a timestamp
            timestamp = time.strftime("%Y%m%d_%H%M%S")

            # Create the archive directory if it doesn't exist
            archive_dir = os.path.join(settings.MEDIA_ROOT, 'archive')
            os.makedirs(archive_dir, exist_ok=True)

            # Define the new file name with the timestamp
            base_name = os.path.basename(existing_media.file.name)
            name, ext = os.path.splitext(base_name)
            new_name = f"{name}_{timestamp}{ext}"
            archive_path = os.path.join(archive_dir, new_name)

            # Move the existing file to the archive folder
            os.rename(existing_media.file.path, archive_path)

            # Delete the reference to the old file
            existing_media.file.delete(save=False)

        super().save(*args, **kwargs)


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    tranaction_choices = [
        ('B', 'Basket'),
        ('F', 'Favourite'),
        ('Q', 'Quote'),
        ('R', 'Return'),
        ('S', 'Sale'),
    ]
    type = models.CharField(
        max_length=1,
        choices=tranaction_choices,
        default='',
    )

    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.quantity}"


class SalesOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)  # Automatically set on creation
    number = models.CharField(max_length=50, unique=True)  # Unique sales order number
    billing_name = models.CharField(max_length=255)
    billing_address = models.TextField()
    billing_code = models.CharField(max_length=20, blank=True)  # Optional billing phone number
    billing_phone = models.CharField(max_length=20, blank=True)  # Optional billing phone number
    shipping_name = models.CharField(max_length=255, blank=True)  # Optional shipping name
    shipping_address = models.TextField(blank=True)  # Optional shipping address
    shipping_code = models.CharField(max_length=20, blank=True)  # Optional shipping phone number
    shipping_phone = models.CharField(max_length=20, blank=True)  # Optional shipping phone number
    items_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    vat_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    order_total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status_choices = [
        ('1', 'Preparing'),
        ('2', 'Shipped'),
        ('3', 'Complete'),
    ]
    status = models.CharField(
        max_length=1,
        choices=status_choices,
        default='',
    )
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Sales Order: {self.number}"
    

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Sales Order Item: {self.product.name} (x{self.quantity})"

    class Meta:
        unique_together = (('sales_order', 'product'),)


"""
class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class Support(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
"""


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    reference_number = models.CharField(max_length=20, null=True, blank=True)


class Support(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    order_number = models.TextField()
    message = models.TextField()
    reference_number = models.CharField(max_length=20, null=True, blank=True)