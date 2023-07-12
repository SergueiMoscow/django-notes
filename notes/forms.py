from django import forms

from notes.models import Note, Tag


class NoteModelForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Note
        fields = ['title', 'body', 'image']
        labels = {
            'title': 'Заголовок',
            'body': 'Текст',
            'image': 'Изображение',
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите заголовок', 'class': "form-control"}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TagModelForm(forms.ModelForm):
    tag = forms.CharField(required=False, widget=forms.TextInput(attrs={'required': False, 'placeholder': 'Введите тег', 'class': "form-control"}))

    class Meta:
        model = Tag
        fields = ['tag']
        # widgets = {
        #     'tag': forms.TextInput(attrs={'required': False, 'placeholder': 'Введите тег', 'class': "form-control"}),
        # }
