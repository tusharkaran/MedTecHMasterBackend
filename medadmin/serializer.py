# serializers.py
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Admin  # Adjust path as needed

class AdminCreateSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(write_only=True, min_length=6)

    def create(self, validated_data):
        # Hash the password before saving using Django's make_password
        hashed_password = make_password(validated_data['password'])
        admin = Admin.objects.create(
            user_name=validated_data['user_name'],
            password=hashed_password
        )
        return admin


