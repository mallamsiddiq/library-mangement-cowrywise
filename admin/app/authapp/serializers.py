from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

class AdminRegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ["firstname", "lastname", "email", 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required':True}
        }
        
    def validate_email(self, value):
        """
        Check that the email domain is 'cowrywise.com'.
        """
        if not value.endswith('@cowrywise.com'):
            raise serializers.ValidationError(_(" Invalid domain grant .."))
        return value
        
    def create(self, validated_data):
        user = get_user_model().objects.create_superuser(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("firstname", "lastname", "email",)