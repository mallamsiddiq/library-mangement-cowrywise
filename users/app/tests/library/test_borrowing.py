# tests/test_views.py
import datetime
from datetime import timedelta
from django.utils import timezone

from django.urls import reverse
from django.db import models
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from library.models import Book, Issuance
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin

class BookViewSetTests(IgnoreEventBusActionsMixin, TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            firstname='John', lastname='Doe', email='john.doe@example.com', password='password123'
        )
    
        self.book = Book.objects.create(
            title='Test Book', author='Test Author', publisher='Wiley', category='fiction',
            total_copies=10, copies_borrowed=0
        )
        

        self.borrow_url = reverse('library:books-borrow', kwargs={'pk': self.book.pk})
        self.return_url = reverse('library:books-return', kwargs={'pk': self.book.pk})

    def test_borrow_book_success(self):
        
        current_copies_borrowed = self.book.copies_borrowed
        current_total_issuamces = Issuance.objects.count()
        
        response = self.client.post(self.borrow_url, 
                                    data={'return_in_days': (return_in_days:= 4),
                                          'user': self.user.id})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_borrowed, current_copies_borrowed + 1)
        self.assertEqual(Issuance.objects.count(), current_total_issuamces + 1)
        
        expected_return_date = timezone.now() + timedelta(days=return_in_days)
        expected_return_date_str = expected_return_date.isoformat()[:11]
        
        data = response.data
        self.assertEqual(data['date_to_return'][:11], expected_return_date_str)
        
    def test_borrow_book_no_id_no_auth(self):
        response = self.client.post(self.borrow_url, 
                                    data={'return_in_days': 4})
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_borrow_book_success_no_id_but_auth(self):
        
        self.client.force_authenticate(user=self.user)
        
        current_copies_borrowed = self.book.copies_borrowed
        current_total_issuamces = Issuance.objects.count()
        
        response = self.client.post(self.borrow_url, 
                                    data={'return_in_days': (return_in_days:= 4)})
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.book.refresh_from_db()
        self.assertEqual(self.book.copies_borrowed, current_copies_borrowed + 1)
        self.assertEqual(Issuance.objects.count(), current_total_issuamces + 1)
        
        expected_return_date = timezone.now() + timedelta(days=return_in_days)
        expected_return_date_str = expected_return_date.isoformat()[:11]
        
        data = response.data
        self.assertEqual(data['date_to_return'][:11], expected_return_date_str)
    
        
    def test_borrow_book_out_of_stock(self):
        # Set book to be fully borrowed
        self.book.copies_borrowed = self.book.total_copies
        self.book.save()
        
        response = self.client.post(self.borrow_url, data={
                            'return_in_days': 4,
                            'user':self.user.id})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.data['errors'][0])
        self.assertEqual('not_found', response.data['errors'][0]['code'])

    def test_borrow_same_owing_copy_of_book(self):
        """Test trying to borrow a book the user has already borrowed but not returned"""
        # First borrow the book
        self.client.post(self.borrow_url, data={
                            'return_in_days': 4,
                            'user':self.user.id})
        
        # Try to borrow the book again
        response = self.client.post(self.borrow_url, data={'user':self.user.id,
                                                           'return_in_days': 4,})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data['errors'][0])
        self.assertEqual('book_not_available', response.data['errors'][0]['code'])          
    
    def test_return_book_success(self):
        """Test returning a borrowed book"""
        # Borrow the book first
        issuance = Issuance.objects.create(book=self.book, user=self.user)
        # confirm book is not returned
        self.assertIsNone(issuance.returned_at)
        
        # Return the book
        response = self.client.post(self.return_url, data={'user':self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        issuance.refresh_from_db()
        self.assertIsNotNone(issuance.returned_at)

    def test_return_book_not_borrowed(self):
        """Test trying to return a book that was never borrowed by the user"""
        response = self.client.post(self.return_url, data={'user':self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], "No active issuance found for this book.")

    def test_return_already_returned_book(self):
        """Test returning a book that was already returned"""
        # Borrow the book and mark it as returned
        
        naive_datetime = datetime.datetime.strptime('2024-09-01', '%Y-%m-%d')
        
        Issuance.objects.create(book=self.book, 
                                user=self.user, 
                                returned_at=timezone.make_aware(naive_datetime))
        
        # Try to return again
        response = self.client.post(self.return_url, data={'user':self.user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('No active issuance found for this book.', response.data['detail'])