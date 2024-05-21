import os
from django.utils import timezone
import time
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


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


class Media(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='uploads/', null=True)
    version = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
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
