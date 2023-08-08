import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from notes.models import UserProfile, Note


class IndexViewTest(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        print(response)
        # self.assertEqual(True, False)  # add assertion here
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'notes/index.html')


class NotesListViewTest(TestCase):
    fixtures = ['users.json', 'userprofile.json', 'notes.json', 'tags.json']

    def test_notes_list(self):
        path = reverse('notes_list')
        notes = Note.objects.filter(private=False).order_by('-created_at').first()
        response = self.client.get(path)
        self.assertEqual(response.context['notes'][0], notes)
        self.__common_tests(response)

    def test_notes_list_with_tag(self):
        pass

    def test_tags_list(self):
        path = reverse('tags_list')
        response: JsonResponse = self.client.get(f'{path}?q=d')
        tags: dict = json.loads(response.content)
        self.assertEqual(response.content[0:1], b'{')
        self.assertLess(0, len(tags))
        self.__common_tests(response)

    def __common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
