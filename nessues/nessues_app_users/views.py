from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username}')
            return redirect('home') # redirect to the home page
        # messages.error(request, )
    else:
        form = UserRegisterForm()
    return render(request, 'nessues_app_users/register.html', {'form': form})

def login_view(request):
    return render(request, 'nessues_app_users/login.html')
