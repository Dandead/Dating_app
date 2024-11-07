from rest_framework import serializers
from .models import DatingUser


class DatingUserForOutsiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatingUser
        fields = ["id", "first_name", "last_name", "gender", "avatar"]


class DatingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatingUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "gender",
            "avatar",
            "birthday",
        ]
        read_only_fields = ("email",)
