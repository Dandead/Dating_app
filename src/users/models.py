from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class DatingUser(AbstractBaseUser, PermissionsMixin):
    """Overring basic user model for DatingApp"""

    email = models.EmailField("Email", unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

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

    def __repr__(self):
        return str(self.nickname)
