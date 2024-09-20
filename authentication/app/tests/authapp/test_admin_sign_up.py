# test_authentication.py
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from tests.case_utils import IgnoreEventBusActionsMixin

class AdminRegistrationTests(IgnoreEventBusActionsMixin, APITestCase):
    patch_target = ['events.producers.send_users_updates.publish_to_network']
    
    def setUp(self):
        self.url = reverse('authapp:authentication-admin-signup')
        
        self.valid_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'john.doe@cowrywise.com',
            'password': 'securepassword123'
        }

    def test_successful_registration(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'User registered successfully')
        
        user = get_user_model().objects.filter(email=self.valid_data['email']).first()
        self.assertIsNotNone(user)
        
        self.assertEqual(user.firstname, self.valid_data['firstname'])
        self.assertEqual(user.lastname, self.valid_data['lastname'])

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_registration_missing_password(self):
        data = self.valid_data.copy()
        data.pop('password')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('password', response.data['errors'][0]['attr'])
        self.assertEqual('required', response.data['errors'][0]['code'])
        
    def test_admin_signup_with_invalid_email_domain(self):
        data = self.valid_data.copy()
        data['email'] = 'janedoe@gmail.com',  # invalid domain
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('email', response.data['errors'][0]['attr'])
        self.assertEqual('invalid', response.data['errors'][0]['code'])
        
    def test_registration_duplicate_email(self):
        get_user_model().objects.create_user(**self.valid_data)
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('email', response.data['errors'][0]['attr'])
        self.assertEqual('unique', response.data['errors'][0]['code'])


