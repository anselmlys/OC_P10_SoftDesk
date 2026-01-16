from django.shortcuts import render
from rest_framework import generics

from users.serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
