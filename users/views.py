from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import RegisterSerializer, MeSerializer


class RegisterView(generics.CreateAPIView):
    '''Allow a user to create a new account'''

    serializer_class = RegisterSerializer


class MeView(generics.RetrieveUpdateDestroyAPIView):
    '''
    - GET: return the information of the authenticated user 
    - PATCH: update some of the user information (ex: consent)
    - DELETE: delete the user account
    '''

    serializer_class = MeSerializer

    def get_object(self):
        return self.request.user
