from rest_framework import generics, permissions
from api.models import DatingUser
from api.serializers import DatingUserSerializer
from api.serializers import CreateDatingUserSerializer
from api.serializers import MatchSerializer


class DatingUserListAPI(generics.ListAPIView):
    queryset = DatingUser.objects.all()
    serializer_class = DatingUserSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class DatingUserCreateAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CreateDatingUserSerializer


class DatingMatchCreateAPI(generics.CreateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = MatchSerializer
