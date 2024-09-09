from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ["firstname", "lastname", "email", 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required':True}
        }
        
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("firstname", "lastname", "email",)