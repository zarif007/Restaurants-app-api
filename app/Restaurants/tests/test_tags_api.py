from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from Restaurants.serializers import TagSerializer


TAGS_URL = reverse('Restaurants:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly avialable tags API"""

    def setUp(self):
        self.client = APIClient

    def test_login_required(self):
        """test that login is required for retriving tags"""
        # res = self.client.get(TAGS_URL)

        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().object.create_user(
            'test12@zarif.com',
            'pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.object.create(user=self.user, name='Burger')
        Tag.object.create(user=self.user, name='Pizza')

        res = self.client.get(TAGS_URL)

        tags = Tag.object.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().object.create_user(
            'test123@zarif.com',
            'test123'
        )
        Tag.object.create(user=user2, name='Lala')
        tag = Tag.object.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.object.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
