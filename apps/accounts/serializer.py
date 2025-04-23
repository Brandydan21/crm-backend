from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# For regular users viewing their own profile (read-only)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'location'
        ]
        read_only_fields = fields  # All fields are read-only

# For admins to create/update other users
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'location'
        ]
        read_only_fields = ['id']  # Admin can edit everything else
