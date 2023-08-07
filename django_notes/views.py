from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
import requests
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, TemplateView
from django.shortcuts import HttpResponseRedirect

from notes.models import UserProfile, EmailVerification
from .forms import LoginForm, SignUpForm, UserProfileForm


class UserLoginView(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    next_page = reverse_lazy('index')


def create_profile_if_not_exists(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = UserProfile(user=request.user)
        user_profile.save()
    return


def logout_view(request):
    logout(request)
    return redirect('index')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('notes_login')
    success_message = 'Вы успешно заргеистрированы'


# def register_view(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(request, username=username, password=raw_password)
#             print(user)
#             user.backend = 'django.contrib.auth.backends.ModelBackend'
#             login(request, user)
#             print('test1')
#             return redirect('index')
#     else:
#         form = SignUpForm()
#         return render(request, 'signup.html', {'form': form})
#     return redirect('index')


@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserProfileForm(instance=user_profile)
    return render(request, 'edit_profile.html', {'form': form})


def google_callback(request):
    adapter = GoogleOAuth2Adapter(client_id='your_client_id', client_secret='your_client_secret')
    token = adapter.get_access_token(request)

    headers = {'Authorization': f'Bearer {token.token}'}
    response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', headers=headers)

    if response.status_code == 200:
        data = response.json()
        email = data.get('email')
        social_account = SocialAccount.objects.get(provider='google', uid=data.get('id'))
        # do something with the user's social account
        return redirect('index')
    else:
        pass
# handle error


class EmailVerificationView(TemplateView):
    template_name = 'registration/email_verification.html'

    def get(self, request, *args, **kwargs):
        super(EmailVerificationView, self).get(request, *args, **kwargs)
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        user_profile = UserProfile.objects.get(user=user)
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user_profile.is_verified_email = True
            user_profile.save()
            return super(EmailVerificationView, self).get(request)
        else:
            return HttpResponseRedirect(reverse('index'))
