from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers, exceptions

from library.models import Book, Issuance


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
        
        
class BorrowBookSerializer(serializers.ModelSerializer):
    return_in_days = serializers.IntegerField(default = 7, write_only = True)
    
    class Meta:
        model = Issuance
        fields = '__all__'
        read_only_fields = ['user', 'book', 'returned_at', 'date_to_return']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['book'] = self.context['view'].get_object()
        if return_in_days := validated_data.pop('return_in_days', None):
            validated_data['date_to_return'] = timezone.now() + timedelta(days=return_in_days)
        
        return super().create(validated_data)