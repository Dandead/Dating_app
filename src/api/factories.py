import factory
from django.contrib.auth import get_user_model


DatingUser = get_user_model()
GENDERS = ["M", "F"]


class DatingUserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating DatingUser instances.
    """

    class Meta:
        model = DatingUser
        django_get_or_create = ("email",)

    first_name = factory.Faker("first_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.first_name}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword123")
    last_name = factory.Faker("last_name")
    birthday = factory.Faker("date_of_birth", minimum_age=18, maximum_age=100)
    gender = factory.Faker(
        "random_element",
        elements=("M", "F"),
    )
