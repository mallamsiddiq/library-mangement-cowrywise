import datetime
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model, authenticate
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from django.db import transaction
from django.utils import timezone
from django.core.cache import cache

from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError

from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


def retrieve_access_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': NestedTokenUserSerializer(user).data
    }


class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ["firstname", "lastname", "email", 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required':True}
        }
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("firstname", "lastname", "email",)