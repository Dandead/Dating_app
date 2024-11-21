# Generated by Django 5.0.3 on 2024-11-21 21:06

import django.db.models.deletion
import profiles.services
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DatingProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=150, verbose_name="First name"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=150, verbose_name="Last name"),
                ),
                ("birthday", models.DateField(null=True, verbose_name="Birthday")),
                (
                    "gender",
                    models.CharField(
                        choices=[("M", "Male"), ("F", "Female")],
                        max_length=1,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProfilePicture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(upload_to=profiles.services.user_media_path),
                ),
                (
                    "profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="avatar",
                        to="profiles.datingprofile",
                    ),
                ),
            ],
        ),
    ]
