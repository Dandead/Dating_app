from django.urls import path

from users.views import UserRegistrationView


urlpatterns = [
    path("registration/", UserRegistrationView.as_view(), name="user-register"),
]
