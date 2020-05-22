from http.client import HTTPResponse

import requests
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from members.forms import LoginForm, SignupForm
from members.models import User


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


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()

    # 네이버 로그인
    n_login_base_url = 'https://nid.naver.com/oauth2.0/authorize'
    n_login_params = {
        'response_type': 'code',
        'client_id': '_P0gJW9IsjsuCscC6V5Y',
        'redirect_uri': 'http://localhost:8000/members/naver-login/',
        'state': 'RANDOM_STATE',
    }
    n_login_url = '{base}?{params}'.format(
        base=n_login_base_url,
        params='&'.join([f'{key}={value}' for key, value in n_login_params.items()])
    )

    # 페이스북 로그인
    context = {
        'form': form,
        'app_id': app_id,
        'n_login_url': n_login_url,
    }
    return render(request, 'members/login.html', context=context)


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


app_id = 602161200404788
app_secret = '8f0614ff67b38e2908983c5ef913dd4c'


def facebook_login(request):
    code = request.GET['code']
    redirect_uri = f'http://localhost:8000/members/facebook-login'
    url_access_token = "https://graph.facebook.com/v2.11/oauth/access_token"
    params_access_toekn = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "client_secret": app_secret,
        "code": code,
    }

    response = requests.get(url_access_token, params=params_access_toekn)
    # url_debug_token = 'https://graph.facebook.com/debug_token'
    # params_debug_token = {
    #     "input_token": response.json()['access_token'],
    #     "access_token": f'{app_id}|{app_secret}'
    # }
    # user_info = requests.get(url_debug_token, params=params_debug_token)

    url_user_info = 'https://graph.facebook.com/me'
    user_info_fields = [
        'id',
        'first_name',
        'last_name',
        'picture',
    ]
    access_token = response.json()['access_token']
    params_user_info = {
        "fields": ','.join(user_info_fields),
        "access_token": access_token
    }
    user_info = requests.get(url_user_info, params=params_user_info)

    return HttpResponse(user_info.json().items())