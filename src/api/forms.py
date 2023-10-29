from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import DatingUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = DatingUser
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = DatingUser
        fields = ("email",)
