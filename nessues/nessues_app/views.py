from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.views.generic import TemplateView, ListView

from .models import Room, Table, Task
from .forms import CreateRoomForm, CreateTableForm, CreateTaskForm, UpdateTaskForm, CompleteTaskForm


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


"""
 Forms to handle:  
    1) CreateTaskForm
    2) UpdateTaskForm
    3) CompleteTaskForm
"""
class TasksView(TemplateView):
    template_name = 'nessues_app/tasks.html'
    create_task_class = CreateTaskForm
    update_task_class = UpdateTaskForm
    complete_task_class = CompleteTaskForm

    def get(self, request, *args, **kwargs): 
        available_tasks = Task.objects.filter(table=self.kwargs['key_id'])
        create = self.create_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})
        update = self.update_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})
        complete = self.complete_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})

        return render(request, self.template_name, {'url_arguments': {'key_id': self.kwargs['key_id'], 'current_user': self.request.user.id}, 'available_tasks': available_tasks, 'create': create, 'update': update, 'complete': complete})

    def post(self, request, *args, **kwargs):
        create = self.create_task_class(request.POST)
        update = self.update_task_class(request.POST)
        complete = self.complete_task_class(request.POST)

        if create.is_valid():
            create.save()
            # messages.success(request, 'Task Successfully added')
            return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')

        if update.is_valid():
            update.save()
            messages.success(request, 'Task successfully updated')
            return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')

        if complete.is_valid():
            id_to_close = complete.cleaned_data['id']
            try:    
                task_to_complete = Task.objects.get(id=id_to_close) 
                task_to_complete.delete()
            except Exception:
                messages.warning(request, 'Wrong id provided, try again')
                return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')

            messages.success(request, 'Task successfully completed')
            return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')
        
        return render(request, self.template_name, {'create': create, 'update': update, 'complete': complete})
