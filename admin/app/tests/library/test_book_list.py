from django.urls import reverse
from django.utils.timezone import localtime

from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from library.models import Book, Issuance
from library.models.enums import CategoryChoices, PublisherChoices
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin


class BookListsTestCase(IgnoreEventBusActionsMixin, APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        # Create an admin user for authentication
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@cowrywise.com',
            password='adminpassword',
            firstname='Admin',
            lastname='User'
        )
        
        self.library_user1, self.library_user2 =[
            get_user_model().objects.create_user(
                email=f'user{idx}@email.com',
                password=f'pasword {idx}',
                firstname=f'Name {idx}',
                lastname=f'User {idx}'
            ) for idx in range(1, 3)] 
            
    
        # Log in as the superuser
        self.client.force_authenticate(user = self.admin_user)
        
        self.books  = [
            Book.objects.create(
            title=f'Test Book {idx}', author=f'Test Author {idx}', 
            publisher=(PublisherChoices.values()+['Wiley'])[idx], 
            category=(CategoryChoices.values()+['Fiction'])[idx],
            total_copies=idx or 1, copies_borrowed=0
        ) for idx in range(4) ]
        
        self.book1, self.book2, self.book3, self.book4 = self.books
        
        Issuance.objects.create(user=self.library_user1,
                                book = self.book1, 
                                date_to_return =datetime.now() + timedelta(days=3),)
        Issuance.objects.create(user=self.library_user2,
                                book = self.book2, 
                                date_to_return =datetime.now() + timedelta(days=5),)
        
        self.unavailable_books_url = reverse('library:books-unavailables')
        self.user_borrowed_books_url = reverse('library:books-user-borowed',
                                             kwargs={'user_id':self.library_user1.id})

    def test_unavailables_books(self):
        # manually updates copies borrowed as its synchronous activity on the other api service
        self.book2.copies_borrowed += 1
        self.book2.save()
        self.book1.copies_borrowed += 1
        self.book1.save()
        
        """
        Test that only books with all copies borrowed are returned.
        """
        # Send GET request to the unavailables endpoint
        response = self.client.get(self.unavailable_books_url)
        data = response.data['results']
        
        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        # Extract the book titles from the response data
        response_titles = set([book['title'] for book in data])
        
        # Only book1 and 2 should be in the response
        self.assertNotEqual(len(self.books), response.data['count'])
        self.assertEqual(2, response.data['count'])
        self.assertIn(self.book1.title, response_titles)
        self.assertIn(self.book2.title, response_titles)
        self.assertNotIn(self.book4.title, response_titles)
        self.assertNotIn(self.book3.title, response_titles)
        
        # confirm expected return dates are return and as expected
        for book in data:
            issuance = Issuance.objects.filter(book_id = book['id']).first()
            self.assertEqual(str(issuance.date_to_return)[:11], str(book['expected_return_date'])[:11])
            
            
    def test_books_borrowed_by_a_user(self):
        # borrow book 3 join for user1 and 1 for user 2
        Issuance.objects.create(user=self.library_user1,
                                book = self.book3, 
                                date_to_return =datetime.now() + timedelta(days=3),)
        
        """
        Test that only books user 1 borrowed are returned.
        """
        # Send GET request to the unavailables endpoint
        response = self.client.get(self.user_borrowed_books_url)
        data = response.data['results']
        
        # Verify the response status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        # Extract the book titles from the response data
        response_titles = set([book['title'] for book in data])
        
        # Only book1 and 2 should be in the response
        self.assertNotEqual(len(self.books), response.data['count'])
        self.assertEqual(2, response.data['count'])
        self.assertIn(self.book1.title, response_titles)
        self.assertIn(self.book3.title, response_titles)
        self.assertNotIn(self.book2.title, response_titles)
        self.assertNotIn(self.book4.title, response_titles)
        
        for book in data:
            issuance = Issuance.objects.filter(book_id = book['id'], 
                                               user = self.library_user1).first()
            self.assertIsNotNone(issuance)
            self.assertEqual(str(issuance.date_to_return)[:11], str(book['expected_return_date'])[:11])
        