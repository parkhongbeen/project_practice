from django.contrib.auth import login
from django.shortcuts import render, redirect

from members.forms import LoginForm, SignupForm


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            request.session['user'] = form.user_id
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'members/login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render('home/home.html')
    else:
        form = SignupForm()

    return render(request, 'members/signup.html', {'form': form})
