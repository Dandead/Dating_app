from rest_framework import serializers
from .models import DatingUser, Match


class CreateDatingUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

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


class DatingUserSerializer(serializers.ModelSerializer):
    likes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_liked = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = DatingUser
        fields = [
            'email',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'image',
            'likes',
            'is_liked'
        ]


class MatchSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source="sender.email")
    retriever = serializers.ReadOnlyField(source="retriever.email")

    class Meta:
        model = Match
        fields = [
            'sender',
            'retriever'
        ]
