from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager
from hashlib import sha256
import uuid


def user_media_path(instance, filename) -> str:
	"""Create user's media path based on email hash"""
	folder :str = f'user_{sha256(str(instance.email).encode("utf-8")).hexdigest()}'
	hashed_filename :str = f'{uuid.uuid4()}.{str(filename).split(".")[-1]}'
	return f'{folder}/{hashed_filename}'

# class DatingUser(AbstractBaseUser):
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
	REQUIRED_FIELDS = ["first_name", "gender"]

	def __repr__(self):
		return self.email
	