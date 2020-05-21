from http.client import HTTPResponse

import requests
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import LoginForm, SignupForm
from members.models import User


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()

    login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    login_params = {
        'response_type': 'code',
        'client_id': '_P0gJW9IsjsuCscC6V5Y	',
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    login_url = '{base}?{params}'.format(
        base=login_base_url,
        params='&'.join([f'{key}={value}' for key, value in login_params.items()])
    )
    context = {
        'form': form,
        'login_url': login_url,
    }
    return render(request, 'members/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('members:login')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'home/home.html')
    else:
        form = SignupForm()
    return render(request, 'members/signup.html', {'form': form})


def naver_login(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    if not code or not state:
        return HTTPResponse('code 또는 state 전달되지 않았습니다.')
    token_base_url = 'https://nid.naver.com/oauth2.0/token'
    token_params = {
        'grant_type': 'authorization_code',
        'client_id': '_P0gJW9IsjsuCscC6V5Y',
        'client_secret': 'BCGa0WqGnS',
        'code': code,
        'state': state,
        'redirectURI': 'https://localhost:8000/members/naver-login/',
    }
    token_url = '{base}?{params}'.format(
        base=token_base_url,
        params='&'.join([f'{key}={value}' for key, value in token_params.items()])
    )
    response = requests.get(token_url)
    access_token = response.json()['access_token']

    me_url = 'https://openapi.naver.com/v1/nid/me'
    me_headers = {
        'Authorization': f'Bearer {access_token}',
    }
    me_response = requests.get(me_url, headers=me_headers)
    me_response_data = me_response.json()

    unique_id = me_response_data['response']['id']

    naver_username = f'n_{unique_id}'
    if not User.objects.filter(username=naver_username).exists():
        user = User.objects.create_user(username=naver_username)
    else:
        user = User.objects.get(username=naver_username)
    login(request, user)
    return render(request, 'home/home.html')
