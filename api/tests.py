from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import InventoryItem
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken
import ast

class InventoryItemViewSetTests(APITestCase):

    def setUp(self):
        # Create a user and obtain a token
        self.user = User.objects.create_user(name='testuser', email="testpass@gmail.com", password='testpass@123')
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Prepare test data
        self.item = InventoryItem.objects.create(inventory_id=1, name='Test Item', description="Test description")

        # URL for the API endpoints
        self.create_url = reverse('item-list')  # Create and list action share the same URL
        self.detail_url = lambda pk: reverse('item-detail', kwargs={'pk': pk})  # For retrieve, update, delete

    def test_create_item(self):
        """Test creating an inventory item"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {'name': 'New Item', 'description': 'This is a new item'}

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assuming success response returns 200
        self.assertEqual(response.data['data']['name'], 'New Item')
        self.assertEqual(response.data['data']['description'], 'This is a new item')

    def test_retrieve_item(self):
        """Test retrieving an inventory item"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # Retrieve from DB
        response = self.client.get(self.detail_url(self.item.inventory_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Test Item')
        self.assertEqual(response.data['data']['description'], 'Test description')

    def test_update_item(self):
        """Test updating an inventory item"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)
        data = {'name': 'Updated Item', 'description': 'Updated description'}

        response = self.client.put(self.detail_url(self.item.inventory_id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Item')
        self.assertEqual(response.data['data']['description'], 'Updated description')

    def test_delete_item(self):
        """Test deleting an inventory item"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        # First, delete the item
        response = self.client.delete(self.detail_url(self.item.inventory_id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check for successful deletion

        # Try to retrieve the deleted item, expecting a 404 Not Found
        response = self.client.get(self.detail_url(self.item.inventory_id))

        # Expect a 400 status code when trying to access the deleted item
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
