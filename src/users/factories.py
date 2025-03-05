import factory
from django.contrib.auth import get_user_model
from users.models import DatingProfile, DatingUserNickname, ProfilePicture


DatingUser = get_user_model()


class DatingUserFactory(factory.django.DjangoModelFactory):
    """Factory for creating DatingUser instances."""

    class Meta:  # type: ignore
        model = DatingUser
        django_get_or_create = ("email",)

    email = factory.Faker("email", domain="example.com")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword12345")

    nickname = factory.RelatedFactory("users.factories.NicknameFactory", "user")
    profile = factory.RelatedFactory("users.factories.DatingProfileFactory", "user")


class NicknameFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = DatingUserNickname
        django_get_or_create = ("nickname",)

    user = factory.SubFactory("users.factories.DatingUserFactory", nickname=None)
    nickname = factory.Faker("user_name")


class DatingProfileFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = DatingProfile

    user = factory.SubFactory("users.factories.DatingUserFactory", profile=None)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    birthday = factory.Faker("date_of_birth", minimum_age=18, maximum_age=100)
    gender = factory.Faker(
        "random_element",
        elements=("M", "F"),
    )
    avatar = factory.RelatedFactory(
        "users.factories.DatingProfilePictureFactory", "profile"
    )


class DatingProfilePictureFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = ProfilePicture

    profile = factory.SubFactory("users.factories.DatingProfileFactory", avatar=None)
    avatar = factory.django.ImageField(color="blue")
