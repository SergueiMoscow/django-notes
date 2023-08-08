from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from django_notes.forms import SignUpForm


class UserRegistrationTest(TestCase):

    def setUp(self):
        self.path = reverse('notes_register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('signup.html')

    def test_user_registration_post(self):
        data = {
            'username': 'Test_User',
            'email': 'test01@example.com',
            'password1': 'TestPassword01',
            'password2': 'TestPassword01'
        }
        response = self.client.post(self.path, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('notes_login'))
