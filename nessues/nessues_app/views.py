from django.shortcuts import render


def home_view(request):
    return render(request, 'nessues_app/home.html')
