from django.db import models
from users.models import DatingUser


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
        return f"{self.user.nickname or self.user.email}'s profile"
