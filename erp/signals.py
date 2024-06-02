from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StaffProfile


@receiver(post_save, sender=User)
def create_or_update_user_staff_profile(sender, instance, created, **kwargs):
    if instance.is_staff:
        if created:
            StaffProfile.objects.create(user=instance)
        else:
            instance.staff_profile.save()
