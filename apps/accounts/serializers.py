from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    '''
    This serializer is used to validate a user via email and password,
    returning a jwt with user-specific data and group access.
    '''
    username_field = User.EMAIL_FIELD  # tell SimpleJWT we're using email instead of username

    def validate(self, attrs):
        # Extract email and password
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        # Authenticate using username=email (because Django expects username by default)
        user = authenticate(
            request=self.context.get('request'), 
            username=email, 
            password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'name': user.first_name,
            'company': user.company.name if user.company else None,
            'groups': list(user.groups.values_list('name', flat=True)),
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims inside the token
        token['user_id'] = user.id
        token['email'] = user.email
        token['groups'] = list(user.groups.values_list('name', flat=True))

        return token
