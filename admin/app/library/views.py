from django.contrib.auth import get_user_model
from django.db import models

from rest_framework import (viewsets, mixins,permissions)
from rest_framework.decorators import action

from library.serializers import (LibraryUserSerializer, BookSerializer, PlainBookSerializer,
                                 IssuanceSerializer, IssuanceDetailSerializer)
from library.models import Book, Issuance
    

class BookViewSet(viewsets.GenericViewSet, 
                  mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin, mixins.ListModelMixin
                  ):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        if self.action in {'unavailables'}:
            return super().get_queryset().filter(total_copies__lte=models.F('copies_borrowed'))
        
        return super().get_queryset()
    
    @action(detail=False, methods=['get'], url_path='unavailables')
    def unavailables(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

class UsersViewset(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = LibraryUserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=True, methods=['get'], url_path='borrowed-books')
    def borrowed_books(self, request, pk=None):
        
        user = self.get_object()
        
        self.serializer_class = PlainBookSerializer
        
        self.queryset = Book.objects.filter(
            issuances__user=user, issuances__returned_at__isnull=True
        ).distinct()

        return super().list(request)
    

class IssuanceViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Issuance.objects.select_related('book', 'user').all()
    serializer_class = IssuanceSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_serializer_class(self):
        if self.action in {'retrieve'}:
            return IssuanceDetailSerializer
        return super().get_serializer_class()
    
