"""
Tests for the Django admin modifications.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        """Create user and client."""
        self.client = Client()
        # create a superuser to login to admin panel
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password',
        )
        self.client.force_login(self.admin_user)

        # create generic user
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password',
            name='Test User'
        )

    def test_users_list(self):
        """Test that users are listed on page."""
        # get the url of the page that lists the users of the system
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # page should contain the users' name and email
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works."""
        # url: admin/core/user/id/change/
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        # verify page loads successfully
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test the create user page works."""
        # functionality to add users on admin portal
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
