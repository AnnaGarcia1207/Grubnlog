from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .models import Profile


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(profile_of=instance)


@receiver(post_save, sender=User)
def save_account(sender, instance, **kwargs):
    instance.profile.save()


