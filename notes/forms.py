from django import forms

from notes.models import Note, Tag


class NoteModelForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Note
        fields = ['title', 'body', 'image', 'private']
        labels = {
            'title': 'Заголовок',
            'body': 'Текст',
            'image': 'Изображение',
            'private': 'Приватная заметка',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите заголовок', 'class': "form-control"}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'private': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TagModelForm(forms.ModelForm):
    tag = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': False, 'placeholder': 'Введите тег', 'class': "form-control"}))

    class Meta:
        model = Tag
        fields = ['tag']
