from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().object.create_superuser(
            email = 'admin@zarif.com',
            password = 'pass123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().object.create_user(
            email = 'test1213@zarif.com',
            password = 'pass123',
            name = 'django bhai'
        )

    def test_users_listed(self):
        """Test that users are listed on uer page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit pahe works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user pahe works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)