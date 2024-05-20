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
    price = models.DecimalField(max_digits=10, decimal_places=2, default='0.00', validators=[validate_non_negative])
    brand = models.CharField(max_length=255, default='cadence')
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


"""
class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')


class Transaction(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class Support(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
"""
