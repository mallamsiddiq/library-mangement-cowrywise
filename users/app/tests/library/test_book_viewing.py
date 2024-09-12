# tests/test_views.py

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.db import models
from library.models import Book, Issuance
from library.models.enums import PublisherChoices, CategoryChoices
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin

class BookViewingTests(IgnoreEventBusActionsMixin, TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            firstname='John', lastname='Doe', email='john.doe@example.com', password='password123'
        )
        self.books = [Book.objects.create(
            title=f'Test Book {idx}', author='Test Author', 
            publisher=(PublisherChoices.values()+['Wiley'])[idx], 
            category=(CategoryChoices.values()+['Fiction'])[idx],
            total_copies=10, copies_borrowed=0
        ) for idx in range(4) ]
        
        self.book = self.books[-1]

        self.book_url = reverse('library:books-detail', kwargs={'pk': self.book.id})
        self.books_url = reverse('library:books-list')

    def test_get_a_book(self):

        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response contains the expected fields
        self.assertEqual(response.data['title'], self.book.title)
        self.assertEqual(response.data['author'], self.book.author)
        self.assertEqual(response.data['publisher'], self.book.publisher)
        self.assertEqual(response.data['category'], self.book.category)
        self.assertEqual(response.data['total_copies'], self.book.total_copies)
        self.assertEqual(response.data['copies_borrowed'], self.book.copies_borrowed)

    def test_list_books(self):
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(self.books), len(data))
        res_book = data[0]
        
        self.assertEqual(res_book['title'], self.book.title)
        self.assertEqual(res_book['author'], self.book.author)
        self.assertEqual(res_book['publisher'], self.book.publisher)
        self.assertEqual(res_book['category'], self.book.category)
        self.assertEqual(res_book['total_copies'], self.book.total_copies)
        self.assertEqual(res_book['copies_borrowed'], self.book.copies_borrowed)
        
    def test_list_only_available_books(self):
        # make a book unavailable by borrowing all
        self.book.copies_borrowed = self.book.total_copies
        self.book.save()
        response = self.client.get(self.books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertGreater(len(self.books), len(data))
        self.assertNotIn(self.book.title, [book['title'] for book in data])
        
    def test_get_only_available_book(self):
        # make a book unavailable by borrowing all copies
        self.book.copies_borrowed = self.book.total_copies
        self.book.save()
        response = self.client.get(self.book_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_filter_books_by_publisher(self):
        for publisher in PublisherChoices.values():
            response = self.client.get(self.books_url, {'publisher': publisher})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']), (1, 2)[publisher == 'Wiley'])

    def test_filter_books_by_category(self):
        for category in CategoryChoices.values():
            response = self.client.get(self.books_url, {'category': category})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']),  (1, 2)[category == 'Fiction'])


    def test_book_not_found(self):
        response = self.client.get(reverse('library:books-detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
