from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


# User Profile DB table, this table is customized
# however it also relies on a table built
# this table is User table
# it is imported above
# This user table has fields such as username, password and the email


class UserProfile(models.Model):
    # whenever the user gets deleted, the profile record gets deleted as well
    profile_user = models.OneToOneField(User, on_delete=models.CASCADE)

    # we also use image field which is custom field
    # here we set default image that we will create later on...
    profile_image = models.ImageField(default='images/default.png')


# it is decorator
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    # when User table is created, UserProfile table gets a new record
    if created:
        UserProfile.objects.create(profile_user=instance)
    instance.userprofile.save()
