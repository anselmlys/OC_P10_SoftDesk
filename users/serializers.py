from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):

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