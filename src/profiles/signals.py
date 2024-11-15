from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import DatingUser
from profiles.models import DatingProfile


@receiver(post_save, sender=DatingUser)
def create_dating_profile(sender, instance, created, **kwargs):
    """Automaticaly creates Profile with User"""
    if created:
        DatingProfile.objects.create(user=instance)
