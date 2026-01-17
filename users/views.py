from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash

from users.serializers import RegisterSerializer, MeSerializer, ChangePasswordSerializer


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


class ChangePasswordView(APIView):
    '''Update the password of the authenticated user.'''

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        # Launch validate()
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_password = serializer.validated_data['new_password']

        # Hash the password
        user.set_password(new_password)
        user.save()

        # When authentication is by session, allow the user to stay logged-in
        # Not necessary if using JWT
        update_session_auth_hash(request, user)

        return Response('Le mot de passe a été modifié.', status=status.HTTP_200_OK)
