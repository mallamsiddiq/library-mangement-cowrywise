from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from library.models import Book
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin


class BookRemovalTestCase(IgnoreEventBusActionsMixin, APITestCase):
    def setUp(self):
        # Create a user to authenticate as an admin
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email='admin@cowrywise.com',
            password='adminpassword',
            firstname='Admin',
            lastname='User'
        )
        # Log in as the superuser
        self.client.force_authenticate(user=self.user)
        
        # Create a book to be deleted
        self.book = Book.objects.create(
            title='Book to be deleted',
            author='Author',
            publisher='Publisher',
            category='Category',
            total_copies=5,
        )
        self.book_detail_url = reverse('library:books-detail', kwargs={'pk': self.book.pk})

    def test_delete_book(self):
        # Check if the book exists before deletion
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())
        
        # Send DELETE request to remove the book
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Check that the book is removed
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
