from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import Room, Table, Task
from .forms import CreateRoomForm, CreateTableForm, CreateTaskForm


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
            form = CreateRoomForm()
            return HttpResponseRedirect('/rooms')

    content = {
        'available_rooms': Room.objects.filter(owner=request.user.id),
        'form': form
    }

    title = "rooms"
    return render(request, 'nessues_app/mono_rooms.html', {'title': title, 'content': content})

def tables_view(request, key_id):
    form = CreateTableForm(initial={'room': key_id})
    if request.method == "POST":
        form = CreateTableForm(request.POST)
        if form.is_valid():
            form.save()
            form = CreateTableForm()
            return HttpResponseRedirect(f'/tables/{key_id}')
        
    content = {
        'available_tables': Table.objects.filter(room=key_id),
        'room': Room.objects.filter(id=key_id),
        'form': form
    }

    title = "tables"
    return render(request, 'nessues_app/tables.html', {'title': title, 'content': content})


def tasks_view(request, key_id):
    form = CreateTaskForm(initial={'table': key_id, 'created_by': request.user.id})
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            form = CreateTaskForm()
            return HttpResponseRedirect(f'/tables/tasks/{key_id}')

    content = {
        'available_tasks': Task.objects.filter(table=key_id),
        'form': form
    }

    title = "tasks"
    return render(request, 'nessues_app/tasks.html', {'title': title, 'content': content})