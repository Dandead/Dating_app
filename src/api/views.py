from rest_framework import generics, permissions
from api.models import DatingUser
from api.serializers import DatingUserSerializer
from api.serializers import DatingUserForOutsiderSerializer
from api.permissions import IsOwnerOrReadOnly


class UserListView(generics.ListAPIView):
    queryset = DatingUser.objects.all()
    serializer_class = DatingUserForOutsiderSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetailsUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DatingUser.objects.all()
    serializer_class = DatingUserForOutsiderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.kwargs["pk"] and (self.request.user.id == self.kwargs["pk"]):
            return DatingUserSerializer
        else:
            return super().get_serializer_class()


class UserRegistrationView(generics.CreateAPIView):
    queryset = DatingUser.objects.all()
    serializer_class = DatingUserSerializer
    permission_classes = [permissions.AllowAny]
