from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from library.models import Book
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin

class BookCreationTestCase(IgnoreEventBusActionsMixin, APITestCase):
    def setUp(self):
        # Create a user to authenticate as an admin
        self.user = get_user_model().objects.create(
            email='admin@cowrywise.com',
            password='adminpassword',
            firstname='Admin',
            lastname='User'
        )
        self.client = APIClient()
        # Log in as the superuser
        self.client.force_authenticate(user=self.user)
        self.book_list_url = reverse('library:books-list')

    def test_create_book(self):
        """
        Test that a book can be created with all required fields.
        """
        book_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'publisher': 'Wiley',
            'category': 'Fiction',
            'total_copies': 10,
        }
        response = self.client.post(self.book_list_url, data=book_data, format='json')

        # Check the response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Retrieve the created book
        created_book = Book.objects.first()
        self.assertEqual(created_book.title, book_data['title'])
        self.assertEqual(created_book.author, book_data['author'])
        self.assertEqual(created_book.publisher, book_data['publisher'])
        self.assertEqual(created_book.category, book_data['category'])
        self.assertEqual(created_book.total_copies, book_data['total_copies'])
        self.assertEqual(created_book.copies_borrowed, 0) # Default value


