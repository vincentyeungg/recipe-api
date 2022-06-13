"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        # post request to create user endpoint
        res = self.client.post(CREATE_USER_URL, payload)

        # ensure response was successful
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # get the created user by their email
        user = get_user_model().objects.get(email=payload['email'])
        # ensure the passwords are the same
        self.assertTrue(user.check_password(payload['password']))
        # ensure the password is NOT returned from the response
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        # should get 400 bad request when creating user with existing
        # credentials
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        # ensure we get bad request on passwords too short
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # try to look for the user with the attempted email and short password
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        # ensure that user is not created at all
        self.assertFalse(user_exists)
