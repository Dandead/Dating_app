from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager
from users.services import add_watermark_to_image, user_media_path


class DatingUser(AbstractBaseUser, PermissionsMixin):
    """Overring basic user model for DatingApp"""

    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField(default=True)  # type: ignore
    is_staff = models.BooleanField(default=False)  # type: ignore
    is_superuser = models.BooleanField(default=False)  # type: ignore
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:  # type: ignore
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ("-date_joined", "is_active")

    def __repr__(self):
        return str(self.email)

    def __str__(self):
        return str(self.email)


class DatingUserNickname(models.Model):
    """Model provides user's unique nickname"""

    user = models.OneToOneField(
        DatingUser, on_delete=models.CASCADE, related_name="nick"
    )
    nickname = models.CharField("Nickname", max_length=20, unique=True)

    objects = models.Manager()

    def __repr__(self):
        return str(self.nickname)

    def __str__(self):
        return str(self.nickname)


class DatingProfile(models.Model):
    user = models.OneToOneField(
        DatingUser, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    birthday = models.DateField("Birthday", null=True)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField("Gender", max_length=1, choices=GENDER_CHOICES)

    objects = models.Manager()

    def __repr__(self):
        return f"{self.user.email}'s profile"  # type: ignore

    def __str__(self):
        return f"{self.user.email}'s profile"  # type: ignore


class ProfilePicture(models.Model):
    profile = models.OneToOneField(
        DatingProfile, on_delete=models.CASCADE, related_name="avatar"
    )
    avatar = models.ImageField(upload_to=user_media_path)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # add watermark to user uploaded photos after saving db instance
        if self.avatar:
            image_to_update = self.avatar.path  # type: ignore
            add_watermark_to_image(image_to_update)
