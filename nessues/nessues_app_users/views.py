from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import UserRegisterForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'nessues_app_users/register.html', {'form': form, 'title': 'register'})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'User {username} successfully authenticated!')
                return redirect('home')
            else:
                messages.error(request, 'No user with provided credentials found')
        else:
            messages.error(request, 'Form is not valid')
    else:
        form = AuthenticationForm()
    return render(request, 'nessues_app_users/login.html', {'form': form, 'title': 'login'})


def logout_view(request):
    logout(request)
    messages.info(request, 'You are successfully logged out!')
    return redirect('home')

@login_required(login_url='/login')
def account_view(request):
    content = {}
    return render(request, 'nessues_app_users/account.html', context=content)
        

