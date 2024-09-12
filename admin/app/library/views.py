from django.contrib.auth import get_user_model
from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import (viewsets, mixins, permissions)
from rest_framework.decorators import action

from library.serializers import (LibraryUserSerializer, BookSerializer, PlainBookSerializer,
                                 IssuanceSerializer, IssuanceDetailSerializer)
from library.models import Book, Issuance
from authapp.permission import IsLibraryAdminUser
    

class BookViewSet(viewsets.GenericViewSet, 
                  mixins.CreateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin, mixins.ListModelMixin
                  ):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        if self.action == 'unavailables':
            return super().get_queryset().filter(total_copies__lte=models.F('copies_borrowed'))
        
        if self.action == 'borrowed_books':
            return super().get_queryset().filter(
                        issuances__user_id=self.kwargs.get('user_id'),
                        issuances__returned_at__isnull=True
                    ).distinct()
        
        return super().get_queryset()
    
    @action(detail=False, methods=['get'], url_path='unavailables')
    def unavailables(self, request, *args, **kwargs):
        # self.queryset = self.get_queryset()
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_name='user-borowed',
            url_path='borrowed-by_user/(?P<user_id>[0-9a-fA-F-]{36})')
    def borrowed_books(self, request, **kwargs):
        self.queryset = self.get_queryset()
        return super().list(request)
    

class LibraryUsersViewset(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = LibraryUserSerializer
    permission_classes = [permissions.AllowAny]
    

class IssuanceViewSet(viewsets.ReadOnlyModelViewSet):
    
    queryset = Issuance.objects.select_related('book', 'user').all()
    serializer_class = IssuanceSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_serializer_class(self):
        if self.action in {'retrieve'}:
            return IssuanceDetailSerializer
        return super().get_serializer_class()
    
