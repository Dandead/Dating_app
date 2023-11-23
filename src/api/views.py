from rest_framework import generics, permissions
from api.models import DatingUser
from api.serializers import DatingUsersSerializer, DatingUserRegistrationSerializer


class DatingAPIlist(generics.ListAPIView):
    queryset = DatingUser.objects.all()
    serializer_class = DatingUsersSerializer

class DatingAPICreate(generics.CreateAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DatingUserRegistrationSerializer
