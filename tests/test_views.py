from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class IndexViewTest(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        print(response)
        # self.assertEqual(True, False)  # add assertion here
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'notes/index.html')


class NotesListViewTest(TestCase):
    fixtures = ['notes.json', 'tags.json']

    def test_notes_list(self):
        path = reverse('notes_list')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

