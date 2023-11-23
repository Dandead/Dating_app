from rest_framework import serializers
from .models import DatingUser


class DatingUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatingUser
        fields = [
            'email',
            'password',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'image',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = DatingUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class DatingUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatingUser
        fields = [
            'first_name',
            'last_name',
            'gender',
            'image',
        ]