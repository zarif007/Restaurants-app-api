from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test123@zarif.com', password='test123'):
    """Create sample user"""
    return get_user_model().object.create_user(email, password)



class ModelTests(TestCase):

    def test_create_user_email_successfully(self):
        """Creating a new user with an email is Successfull"""
        email = 'test@zarif.com'
        password = 'Test123'
        user = get_user_model().object.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """New User is normalized"""
        email = 'test@ZARIF.COM'
        user = get_user_model().object.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_emails(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().object.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().object.create_superuser(
            'test123@zarif.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.object.create(
            user = sample_user(),
            name = 'Title'
        )

        self.assertEqual(str(tag), tag.name)
        