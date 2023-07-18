from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialAccount
import requests

from .forms import LoginForm, SignUpForm


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
            # user = authenticate(username, raw_password)
            login(request) #, user)
            print('test1')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    return redirect('index')



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
