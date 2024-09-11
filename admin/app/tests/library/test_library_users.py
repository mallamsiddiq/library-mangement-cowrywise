from django.urls import reverse
from django.utils import timezone

from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from library.models import Issuance, Book
from library.models.enums import CategoryChoices, PublisherChoices
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin

class LibraryUsersViewSetTestCase(IgnoreEventBusActionsMixin, APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        # Create an admin user for authentication
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@cowrywise.com',
            password='adminpassword',
            firstname='Admin',
            lastname='User'
        )
        
        self.library_users =[
            get_user_model().objects.create_user(
                email=f'user{idx}@email.com',
                password=f'pasword {idx}',
                firstname=f'Name {idx}',
                lastname=f'User {idx}'
            ) for idx in range(1, 5)] 
        
        self.library_user1, self.library_user2, *____ = self.library_users
            
    
        # Log in as the superuser
        self.client.force_authenticate(user = self.admin_user)
        
        self.user_list_url = reverse('library:users-list')
        self.user_detail_url = reverse('library:users-detail', 
                                       kwargs={'pk': self.library_user1.pk})
        self.issuance_list_url = reverse('library:book-borrowing-list')

    def test_list_users(self):
        """
        Test that the user list is accessible and returns the correct users.
        """
            
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(self.library_users) + 1, len(data))
        
        for idx in range(len(self.library_users)):
            user_data = data[idx]
        
            self.assertEqual(user_data['email'], eval(f'self.library_users[-idx -1].email'))
            self.assertEqual(user_data['firstname'], eval(f'self.library_users[-idx -1].firstname'))
            self.assertEqual(user_data['lastname'], eval(f'self.library_users[-idx -1].lastname'))
        
    def test_user_detail(self):
        """
        Test that the user detail view returns correct user data.
        """
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.library_user1.email)
        self.assertEqual(response.data['firstname'], self.library_user1.firstname)
        self.assertEqual(response.data['lastname'], self.library_user1.lastname)
        
        
    def test_list_issuances(self):
        """
        Test that the issuance list is accessible and returns the correct issuances.
        """
        self.books  = [
            Book.objects.create(
            title=f'Test Book {idx}', author=f'Test Author {idx}', 
            publisher=(PublisherChoices.values()+['Wiley'])[idx], 
            category=(CategoryChoices.values()+['Fiction'])[idx],
            total_copies=idx or 1, copies_borrowed=0
        ) for idx in range(4) ]
        
        self.book1, self.book2, self.book3, self.book4 = self.books
            
        issuances = [Issuance.objects.create(
            user=self.library_users[idx%2],
            book=self.books[idx],
            date_to_return=timezone.now() + timedelta(days=7),
        ) for idx in range(len(self.books))]
        
            
        response = self.client.get(self.issuance_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data['results']
        self.assertEqual(len(issuances), len(data))
        
        for idx in range(len(data)):
            print(idx, end= '  ')
            issuance_data = data[idx]
        
            self.assertEqual(issuance_data['user'], eval(f'self.library_users[idx+1]'))
            self.assertEqual(issuance_data['book'], eval(f'self.library_users[idx+1]'))

    def test_issuance_detail(self):
        """
        Test that the issuance detail view returns correct issuance data, including related book and user.
        """
        
        
        
        self.book = Book.objects.create(
            title=f'Test Book', author=f'Test Author ', 
            publisher='Wiley', 
            category='Fiction',
            total_copies = 1, copies_borrowed=0
        )
        
        issuance = Issuance.objects.create(
            user=self.library_user1,
            book=self.book,
            date_to_return=timezone.now() + timedelta(days=7),)
        
        issuance_detail_url = reverse('library:book-borrowing-detail', 
                                           kwargs={'pk': issuance.pk})
        
        response = self.client.get(issuance_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book']['id'], str(self.book.id))
        self.assertEqual(response.data['user']['email'], self.library_user1.email)
