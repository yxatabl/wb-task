from rest_framework import generics
from users.serializers import UserBalanceUpdateSerializer, UserSerializer
from users.models import User

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateBalance(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserBalanceUpdateSerializer