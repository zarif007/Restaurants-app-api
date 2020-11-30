from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Item

from Restaurants.serializers import ItemSerializer


ITEMS_URL = reverse('Restaurants:item-list')


class PublicItemsApiTests(TestCase):
    """Test the publicly available items API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required to access the endpoint"""
        res = self.client.get(ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateItemsApiTests(TestCase):
    """Test the private Items api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'test@zarif.com',
            'test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_items_list(self):
        """Test retrieving a list of items"""
        Item.object.create(user=self.user, name='Fries')
        Item.object.create(user=self.user, name='Shake')

        res = self.client.get(ITEMS_URL)

        item = Item.object.all().order_by('-name')
        serializer = ItemSerializer(item, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_items_limited_to_user(self):
        """test that items for the authenticated user are returned"""
        user2 = get_user_model().object.create_user(
            'ot@zarif.com',
            'ot123'
        )
        Item.object.create(user=user2, name='FriedRice')
        item = Item.object.create(user=self.user, name='Puttin')

        res = self.client.get(ITEMS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], item.name)

    def test_create_item_successful(self):
        """test create a new item"""
        payload = {'name': 'MaxicanRice'}
        self.client.post(ITEMS_URL, payload)

        exists = Item.object.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_item_invalid(self):
        """test creating invalid item fails"""
        payload = {'name': ''}
        res = self.client.post(ITEMS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
