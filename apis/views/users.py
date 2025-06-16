from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers import SignupSerializer, CustomTokenObatainPairSerializer


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


class Login(TokenObtainPairView):
    queryset = User.objects.all()
    serializer_class = CustomTokenObatainPairSerializer
    permission_classes = [AllowAny]


class ListUser(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
