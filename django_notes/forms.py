from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from notes.models import UserProfile


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text='required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send'))


class ProfileForm(forms.ModelForm):
    MAX_UPLOAD_SIZE = 524288  # 500 kB

    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['avatar'].required = False
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send'))

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', False)
        if avatar:
            if avatar.size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError("Файл слишком большой. Максимальный размер 500кб.")
            return avatar
        else:
            return False

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        if 'avatar' in self.cleaned_data:
            profile.avatar = self.cleaned_data['avatar']
        if commit:
            profile.save()

        return profile


def avatar_context_processor(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None
        return {'avatar': profile.avatar if profile else None}
    else:
        return {}