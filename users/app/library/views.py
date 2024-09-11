from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from rest_framework import (
    filters, status, viewsets, mixins,permissions
)
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters.rest_framework import DjangoFilterBackend

from library.serializers import (BorrowBookSerializer, PlainBookSerializer)
from library.models import Book
from utils.exceptions import BookNotAvailableException
    

class BookViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Book.objects.all()
    serializer_class = PlainBookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['publisher', 'category']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != 'return_book':
            # unavailable books are only open for return 
            queryset = queryset.filter(
                total_copies__gt=models.F('copies_borrowed')
            )
            
        return queryset
    
    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # Check if the user has already borrowed the book and hasn't returned it
        if self.action == 'borrow_book':
            if obj.issuances.filter(user=user, returned_at__isnull=True).exists():
                raise BookNotAvailableException("Book Not Available for You")

        return obj
    
    @action(detail=True, methods=['post'], url_path='borrow', url_name='borrow',
            serializer_class = BorrowBookSerializer)
    def borrow_book(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        issuance = serializer.save()
        issuance_serializer = self.serializer_class(issuance)
        return Response(issuance_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], url_path='return', url_name='return')
    def return_book(self, request, *args, **kwargs):
        book = self.get_object()
        user = request.user

        issuance = user.book_issuances.filter( book=book, returned_at__isnull=True).last()
        if not issuance:
            return Response({"detail": "No active issuance found for this book."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the book as returned
        issuance.mark_returned()

        return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)