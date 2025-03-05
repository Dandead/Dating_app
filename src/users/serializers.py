from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.db import transaction
from django.contrib.auth import get_user_model

from users.models import DatingUser, DatingUserNickname, DatingProfile, ProfilePicture


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        source="avatar.avatar", required=False, allow_null=True
    )

    class Meta:
        model = DatingProfile
        fields = ("id", "user", "first_name", "last_name", "birthday", "avatar")
        read_only_fields = ("id", "user")

    @transaction.atomic
    def create(self, validated_data):  # type: ignore
        user = self.context["user"]
        avatar_data = validated_data.pop("avatar", None)
        profile = DatingProfile.objects.create(user=user, **validated_data)
        if avatar_data:
            ProfilePicture.objects.create(profile=profile, **avatar_data)
        return profile


class ProfileNoAvatarSerializer(ProfileSerializer):
    avatar = None

    class Meta(ProfileSerializer.Meta):
        fields = ("id", "user", "first_name", "last_name", "birthday")


class ProfileNoBirthdaySerializer(ProfileSerializer):
    class Meta(ProfileSerializer.Meta):
        fields = ("id", "user", "first_name", "last_name", "avatar")


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=(
            UniqueValidator(
                queryset=DatingUser.objects.all(), message="This email already in use"
            ),
        ),
    )
    nickname = serializers.CharField(
        source="nick.nickname",
        required=False,
        validators=(
            UniqueValidator(
                queryset=DatingUserNickname.objects.all(),
                message="This nickname already in use",
            ),
        ),
        max_length=20,
    )
    profile = ProfileNoAvatarSerializer()

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "nickname", "profile")
        extra_kwargs = {
            "password": {"write_only": True},
        }
        read_only_fields = ("id",)

    @transaction.atomic
    def create(self, validated_data):  # type: ignore
        profile_data = validated_data.pop("profile", None)
        # Validated data stores related model filds NESTED, like:
        # {'email': 'a@a.aa','nick':{'nickname': testuser'},'profile':{'first_name':'test_name'}}
        nickname_data = validated_data.pop("nick", None)
        user = get_user_model().objects.create_user(
            validated_data["email"], validated_data["password"]
        )
        if nickname_data:
            DatingUserNickname.objects.create(user=user, **nickname_data)
        if profile_data:
            profile_serializer = ProfileNoAvatarSerializer(
                data=profile_data, context={"user": user}
            )
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
        return user
