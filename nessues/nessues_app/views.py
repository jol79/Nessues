from django.shortcuts import render


def home_view(request):
    title = "home"
    return render(request, 'nessues_app/home.html', {'title': title})
