from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm


def register_view(request):
    form = UserCreationForm()
    return render(request, 'nessues_app_users/register.html', {'form': form})

def login_view(request):
    return render(request, 'nessues_app_users/login.html')
