from allauth.account.signals import user_signed_up
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import stripe
from .models import Profile


stripe.api_key = settings.STRIPE_SECRET_KEY
