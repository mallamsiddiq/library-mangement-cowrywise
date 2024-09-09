from rest_framework import serializers
from library.models import Book, Issuance  # Adjust the import based on your project structure
from authapp.models import User


class DataEchangeSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=False, required = True) 
    created_at = serializers.DateTimeField(read_only=False)  
    updated_at = serializers.DateTimeField(read_only=False)


class BookSerializer(DataEchangeSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class IssuanceSerializer(DataEchangeSerializer):
    class Meta:
        model = Issuance
        fields = '__all__' 


class UsersSerializer(DataEchangeSerializer):
    class Meta:
        model = User
        fields = '__all__'  
