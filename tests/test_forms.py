from django.test import TestCase

from notes.forms import NoteModelForm, TagModelForm
from notes.models import Note, Tag


class NoteFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print('\nTesting forms')

    def test_title(self):
        form = NoteModelForm()
        self.assertEqual(form.fields['title'].widget.attrs['placeholder'], 'Введите заголовок')

    def test_meta_fields(self):
        form = NoteModelForm()
        self.assertEqual(form._meta.fields, ['title', 'body', 'image', 'private'])

    def test_meta_model(self):
        form = NoteModelForm()
        self.assertEqual(form._meta.model, Note)

    def test_meta_labels(self):
        labels = {
            'title': 'Заголовок',
            'body': 'Текст',
            'image': 'Изображение',
            'private': 'Приватная заметка',
        }
        form = NoteModelForm()
        self.assertEqual(form._meta.labels, labels)

    def test_body_rows(self):
        form = NoteModelForm()
        self.assertEqual(form._meta.widgets['body'].attrs['rows'], 5)


class TagFormTest(TestCase):
    def test_meta_model(self):
        form = TagModelForm()
        self.assertEqual(form._meta.model, Tag)
