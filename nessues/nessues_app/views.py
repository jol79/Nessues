from django.shortcuts import render
from .models import Room, Table, Task


def home_view(request):
    title = "home"
    return render(request, 'nessues_app/home.html', {'title': title})


def groups_view(request):
    content = {
        
    }

    title = "groups"
    return render(request, 'nessues_app/groups.html', {'title': title, 'content': content})


def rooms_view(request):
    content = {
        'available_room_name': Room.objects.filter(owner=request.user.id)
    } 

    title = "rooms"
    return render(request, 'nessues_app/mono_rooms.html', {'title': title, 'content':content})
