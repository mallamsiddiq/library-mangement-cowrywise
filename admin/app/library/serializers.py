import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from rest_framework import serializers, exceptions

from library.models import Book, Issuance


class LibraryUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ("id", "firstname", "lastname", "email",)


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
    user = LibraryUserSerializer(read_only = True)

    class Meta:
        model = Issuance
        fields = '__all__'
        