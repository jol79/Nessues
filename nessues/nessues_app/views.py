from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.views.generic import TemplateView, ListView

from .models import Room, Table, Task
from .forms import CreateRoomForm, CreateTableForm, CreateTaskForm, UpdateTaskForm, CompleteTaskForm, CloseRoomForm


def home_view(request):
    title = "home"
    return render(request, 'nessues_app/home.html', {'title': title})

def groups_view(request):
    content = {
    }

    title = "groups"
    return render(request, 'nessues_app/groups.html', {'title': title, 'content': content})


"""
 data that need to be rendered on the page: 
    1) title
    2) available_rooms
    3) forms
        new room
        delete room
        rename room
"""
class RoomsView(TemplateView):
    template_name = 'nessues_app/mono_rooms.html'
    title = 'room'
    create_room_class = CreateRoomForm
    close_room_class = CloseRoomForm

    def get(self, request, *args, **kwargs):
        available_rooms = Room.objects.filter(owner=self.request.user.id)
        create = self.create_room_class(initial={'owner': self.request.user.id})
        close = self.close_room_class()

        return render(request, self.template_name, {'title': self.title, 'available_rooms': available_rooms, 'create': create, 'close': close})

    def post(self, request, *args, **kwargs):
        create = self.create_room_class(request.POST)
        close = self.close_room_class(request.POST)

        if create.is_valid():
            print(f"CREATE ROOM FORM DATA: {create.cleaned_data}")
            create.save()
            return HttpResponseRedirect('/rooms')
        else: 
            messages.warning(request, "Something went wrong with create room form")
            print(f"CREATE ROOM FORM DATA: {create.cleaned_data}")
            return HttpResponseRedirect('/rooms')

        if close.is_valid(): 
            id_to_close = close.cleaned_data['id']
            try:    
                room_to_close = Room.objects.get(id=id_to_close) 
                room_to_close.delete()
            except Exception:
                messages.warning(request, "Wrong id given, we don't have room with that id")
                return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')
            messages.success(request, "Room successfully closed!")

        return render(request, self.template_name, {'create': create, 'close': close})



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


# """
#  data that need to be rendered on the page: 
#     1) title
#     2) available_tables
#     3) current_room
#     4) forms
#         new table
#         delete table
#         rename table
# """
# class TablesView(TemplateView):
#     template_name = 'nessues_app/tables.html'
#     create_table_class = CreateTableForm
#     close_table_class = CloseTableForm

#     def get(self, request, *args, **kwargs):
#         available_tables = Table.objects.filter(room=self.kwargs['key_id'])
#         create = self.create_table_class()

#         return render(request, self.template_name, {''})


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


def about_view(request):
    content = {  }

    title = "about"
    return render(request, 'nessues_app/about.html', {'title': title, 'content': content})