from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    '''Serializer for user registration information.'''

    # Make sure the password cannot be retrieved from the API
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'is_15_or_older',
            'can_be_contacted',
            'can_data_be_shared'
        ]

    def validate_is_15_or_older(self, value):
        '''Raise an error if the user is less than 15 years old.'''
        if value is not True:
            raise serializers.ValidationError(
                'Vous devez avoir au moins 15 ans pour vous inscrire.'
            )
        return value
    
    def create(self, validated_data):
        password = validated_data.pop("password")

        # Create_user will hash the password
        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        return user


class MeSerializer(serializers.ModelSerializer):
    '''
    Serializer for authenticated user information.
    Only consent-related data are editable.
    '''

    date_joined = serializers.DateTimeField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'can_be_contacted',
            'can_data_be_shared',
            'date_joined'
        ]


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        '''Verify old and new password.'''

        # Retrieve connected user from request
        user = self.context['request'].user

        # Check old password
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError('Ancien mot de passe incorrect.')
        
        # Check that the new password inputs match
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                'Les nouveaux mot de passes ne sont pas identiques.'
            )
        
        # Apply Django password validators (length, complexity...)
        validate_password(attrs['new_password'], user=user)

        return attrs
