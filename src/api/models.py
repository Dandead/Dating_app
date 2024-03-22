from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from .services import add_watermark_to_image, user_media_path


class DatingUser(AbstractBaseUser, PermissionsMixin):
    """Overring basic user model for DatingApp"""
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Second name", max_length=150)
    date_of_birth = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES)
    image = models.ImageField(upload_to=user_media_path, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name"]

    def __repr__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # add watermark to user uploaded photos
        if self.image:
            image_to_update = self.image.path
            add_watermark_to_image(image_to_update)


class Match(models.Model):
    """Match model"""
    sender = models.ForeignKey(
        DatingUser,
        on_delete=models.CASCADE,
        related_name="likes"
    )
    retriever = models.ForeignKey(
        DatingUser,
        on_delete=models.CASCADE,
        related_name="is_liked"
    )
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("sender", "retriever")
