from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from notes.models import EmailVerification, UserProfile


class UserRegistrationTest(TestCase):

    def setUp(self):
        self.path = reverse('notes_register')
        self.data = {
            'username': 'Test_User',
            'email': 'srserguei@yandex.ru',
            'password1': 'TestPassword01',
            'password2': 'TestPassword01'
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed('signup.html')

    def test_user_registration_post(self):
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('notes_login'))
        user = User.objects.get(username=self.data['username'])
        self.assertTrue(UserProfile.objects.filter(user=user).exists())
        self.assertTrue(EmailVerification.objects.filter(user=user).exists())

    def test_user_registration_error(self):
        User.objects.create(username=self.data.get('username'))
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')
