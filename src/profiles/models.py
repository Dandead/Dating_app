from django.db import models
from users.models import DatingUser
from profiles.services import add_watermark_to_image, user_media_path


class DatingProfile(models.Model):
    user = models.OneToOneField(
        DatingUser, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    birthday = models.DateField("Birthday", blank=True, null=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField("Gender", max_length=1, choices=GENDER_CHOICES)

    def __repr__(self):
        return f"{self.user.email}'s profile"


class ProfilePicture(models.Model):
    profile = models.OneToOneField(
        DatingProfile, on_delete=models.CASCADE, related_name="avatar"
    )
    avatar = models.ImageField(upload_to=user_media_path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # add watermark to user uploaded photos after saving db instance
        if self.avatar:
            image_to_update = self.avatar.path
            add_watermark_to_image(image_to_update)
