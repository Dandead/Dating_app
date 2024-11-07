from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from .services import add_watermark_to_image, user_media_path


class DatingUser(AbstractBaseUser, PermissionsMixin):
    """Overring basic user model for DatingApp"""

    email = models.EmailField("Email", unique=True)
    first_name = models.CharField("First name", max_length=150)
    last_name = models.CharField("Last name", max_length=150)
    birthday = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(editable=False)
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField("Gender", max_length=1, choices=GENDER_CHOICES)
    avatar = models.ImageField(upload_to=user_media_path, blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __repr__(self):
        return str(self.email)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_joined = timezone.now()
        super().save(*args, **kwargs)
        # add watermark to user uploaded photos after saving db instance
        if self.avatar:
            image_to_update = self.avatar.path
            add_watermark_to_image(image_to_update)


class Like(models.Model):
    user = models.ForeignKey(
        DatingUser, on_delete=models.CASCADE, related_name="likes_given"
    )
    liked_user = models.ForeignKey(
        DatingUser, on_delete=models.CASCADE, related_name="likes_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "liked_user")
