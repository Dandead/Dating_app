import factory
from django.contrib.auth import get_user_model
from users.models import DatingUserNickname


DatingUser = get_user_model()


class DatingUserFactory(factory.django.DjangoModelFactory):
    """Factory for creating DatingUser instances."""

    class Meta:
        model = DatingUser
        django_get_or_create = ("email",)

    email = factory.Faker("email", domain="example.com")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword12345")

    nickname = factory.RelatedFactory("users.factories.NicknameFactory", "user")
    profile = factory.RelatedFactory("profiles.factories.DatingProfileFactory", "user")


class NicknameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DatingUserNickname
        django_get_or_create = ("nickname",)

    user = factory.SubFactory("users.factories.DatingUserFactory", nickname=None)
    nickname = factory.Faker("user_name")
