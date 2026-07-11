from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile
from core.serializer import AdressSerializer



class UserProfileSerializer(serializers.ModelSerializer):
    user_address = AdressSerializer()
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'user',
            'phone',
            'full_name',
            'profile_picture',
            'user_address',
            'picture_url',
            'profile_completed',
        )

class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    error = serializers.CharField(required=False)

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = (
            'id',
            'last_name',
            'first_name'
        )


