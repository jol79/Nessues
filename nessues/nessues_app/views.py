from django.shortcuts import render

from .models import Room, Table, Task
from .forms import CreateRoomForm


def home_view(request):
    title = "home"
    return render(request, 'nessues_app/home.html', {'title': title})


def groups_view(request):
    content = {
    }

    title = "groups"
    return render(request, 'nessues_app/groups.html', {'title': title, 'content': content})


def rooms_view(request):
    form = CreateRoomForm(initial={'owner': request.user.id})
    if request.method == "POST":
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            form.save()

    content = {
        'available_room_name': Room.objects.filter(owner=request.user.id),
        'form': form
    }

    title = "rooms"
    return render(request, 'nessues_app/mono_rooms.html', {'title': title, 'content':content})
