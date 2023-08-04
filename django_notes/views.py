from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
import requests

from notes.models import UserProfile
from .forms import LoginForm, SignUpForm, UserProfileForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=raw_password)
            print(user)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            print('test1')
            return redirect('index')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    return redirect('index')


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
