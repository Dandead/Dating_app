import factory
from profiles.models import DatingProfile, ProfilePicture


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
        "profiles.factories.DatingProfilePictureFactory", "profile"
    )


class DatingProfilePictureFactory(factory.django.DjangoModelFactory):
    class Meta:  # type: ignore
        model = ProfilePicture

    profile = factory.SubFactory("profiles.factories.DatingProfileFactory", avatar=None)
    avatar = factory.django.ImageField(color="blue")
