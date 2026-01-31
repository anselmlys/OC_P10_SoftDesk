from rest_framework import generics
from rest_framework.mixins import RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash, get_user_model

from users.serializers import (RegisterSerializer, MeSerializer,
                               ChangePasswordSerializer, AdminUserSerializer)
from common.permissions import IsAdminAuthenticated


User = get_user_model()


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
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdminUserViewSet(RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    '''Admin can only use method GET and DELETE on user.'''

    serializer_class = AdminUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminAuthenticated]


class ChangePasswordView(APIView):
    '''Update the password of the authenticated user.'''

    permission_classes = [IsAuthenticated]

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

        return Response('Password has been modified.', status=status.HTTP_200_OK)
