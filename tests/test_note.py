from django.contrib.auth.models import User
from django.test import TestCase

from notes.models import Note


class NoteModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nTesting models')
        User.objects.create(username='test_user')
        Note.objects.create(title='Main', body='test body', user_id=1)

    def test_title_max_length(self):
        obj = Note.objects.get(id=1)
        max_length = obj._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_meta_ordering(self):
        obj = Note.objects.get(id=1)
        ordering = obj._meta.ordering
        self.assertEqual(ordering, ['-created_at'])

    def test_meta_verbose_name(self):
        obj = Note.objects.get(id=1)
        verbose_name = obj._meta.verbose_name
        self.assertEqual(verbose_name, 'Заметка')
