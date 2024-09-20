from rest_framework import serializers
from library.models import Book, Issuance  # Adjust the import based on your project structure
from library.models import User


class DataEchangeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, required = True) 
    created_at = serializers.DateTimeField(read_only=False)  
    updated_at = serializers.DateTimeField(read_only=False)


class BookSerializer(DataEchangeSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class IssuanceSerializer(DataEchangeSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), read_only=False) 
    book = serializers.PrimaryKeyRelatedField(queryset = Book.objects.all(), read_only=False) 
    
    class Meta:
        model = Issuance
        fields = '__all__' 


class UsersSerializer(DataEchangeSerializer):
    email = serializers.CharField(read_only=False, required = False)  
    class Meta:
        model = User 
        fields = ['id', 'email', 'firstname', 'lastname', 'is_superuser', 
                  'is_staff', 'is_active', 'last_login', 'created_at', 'updated_at']

        