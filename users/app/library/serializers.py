from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers, exceptions

from library.models import Book, Issuance
from utils.exceptions import UserNotFoundException, BookNotAvailableException


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("firstname", "lastname", "email",)


class PlainBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['copies_borrowed']


class BookSerializer(serializers.ModelSerializer):
    expected_return_date = serializers.ReadOnlyField(default = None)
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['copies_borrowed']
        

class IssuanceSerializer(serializers.ModelSerializer):
    book = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = Issuance
        fields = '__all__'

class IssuanceDetailSerializer(serializers.ModelSerializer):
    book = PlainBookSerializer(read_only = True)
    user = UserSerializer(read_only = True)

    class Meta:
        model = Issuance
        fields = '__all__'


class UserBookAuthSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
                        queryset = get_user_model().objects.all(),
                        required = False)
    
    def validate(self, attrs):
        
        if not(user:=attrs.get('user', None)):
            attrs['user'] = user = self.context['request'].user
            if not user.is_authenticated:
                raise UserNotFoundException()
        
        
        return super().validate(attrs)
    
    class Meta:
        model = Issuance
        fields = '__all__'
        read_only_fields = ['book', 'returned_at', 'date_to_return']
        
        
class BorrowBookSerializer(UserBookAuthSerializer):
    return_in_days = serializers.IntegerField(write_only = True, required = True)
    
    def create(self, validated_data):
        return_in_days = validated_data.pop('return_in_days')
        validated_data['date_to_return'] = timezone.now() + timedelta(days=return_in_days)
        book = validated_data['book'] = self.context['view'].get_object()
        user = validated_data['user']

        # Check if the user has already borrowed the book and hasn't returned it
        if book.issuances.filter(user=user, returned_at__isnull=True).exists():
            raise BookNotAvailableException("Book Not Available for You, You have same copy not returned")
        
        return super().create(validated_data)
    
    
class ReturnBookSerializer(UserBookAuthSerializer):
    ""