from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Address

# make profile for created user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.object.create(user=instance)

# save em
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

# # make address for created profile
# @receiver(post_save, sender=Profile)
# def create_address(sender, instance, created, **kwargs):
#     if created:
#         Address.object.create(profile=instance)

# # save profile
# @receiver(post_save, sender=Profile)
# def save_address(sender, instance, **kwargs):
#     instance.address.save()