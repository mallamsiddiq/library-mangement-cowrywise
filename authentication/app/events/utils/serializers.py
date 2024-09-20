from rest_framework import serializers
from authapp.models import User


class DataEchangeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, required = True) 
    created_at = serializers.DateTimeField(read_only=False)  
    updated_at = serializers.DateTimeField(read_only=False)
    

class UsersSerializer(DataEchangeSerializer):
    email = serializers.CharField(read_only=False, required = False)  
    class Meta:
        model = User 
        fields = ['id', 'email', 'firstname', 'lastname', 'is_superuser', 
                  'is_staff', 'is_active', 'last_login', 'created_at', 'updated_at']
        