from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()

class AuthViewSetTests(APITestCase):
    def setUp(self):
        self.signup_url = reverse('sighup-access-list')  # Corrected URL for signup
        self.login_url = reverse('login-list')             # URL for login
        self.logout_url = reverse('logout-list')           # URL for logout
        self.profile_url = reverse('profile-list') 
        self.user_data = {
            'email': 'test@example.com',
            'password': 'securepassword',
            'first_name': 'Test',
            'last_name': 'User'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_signup(self):
        response = self.client.post(self.signup_url, {
            'email': 'newuser@example.com',
            'password': 'newsecurepassword',
            'name': 'newuser'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_login(self):
        response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data['data'])

    def test_login_invalid_user(self):
        response = self.client.post(self.login_url, {
            'email': 'nonexistent@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Error : User Account is not available')

    def test_logout_without_tokens(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_with_tokens(self):
        # Log in to get tokens
        login_response = self.client.post(self.login_url, {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        })
        tokens = login_response.data['data']
        
        # Simulate a logout with the access token in the Authorization header
        response = self.client.post(self.logout_url, 
                                    **{'HTTP_AUTHORIZATION': f'Bearer {tokens["access_token"]}'})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
