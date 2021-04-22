from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.views.generic import TemplateView

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


# def tasks_view(request, key_id):
#     form = CreateTaskForm(initial={'table': key_id, 'created_by': request.user.id})
#     if request.method == "POST":
#         form = CreateTaskForm(request.POST)
#         if form.is_valid():
#             form.save()
#             form = CreateTaskForm()
#             return HttpResponseRedirect(f'/tables/tasks/{key_id}')

#     content = {
#         'available_tasks': Task.objects.filter(table=key_id),
#         'form': form
#     }

#     title = "tasks"
#     return render(request, 'nessues_app/tasks.html', {'title': title, 'content': content})

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
        print(f"Response to GET request: {self.kwargs['key_id']} from {self.request.user.id}")
        create = self.create_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})
        update = self.update_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})
        complete = self.complete_task_class(initial={'table': self.kwargs['key_id'], 'created_by': self.request.user.id})

        return render(request, self.template_name, {'create': create, 'update': update, 'complete': complete})

    def post(self, request, *args, **kwargs):
        post_data = request.POST or None
        create_form = self.create_task_class(post_data, prefix='create')
        # print(f'Current user_id: {request.user.id}\nCurrent room_id: {self.kwargs["key_id"]}')
        update_form = self.update_task_class(post_data, prefix='update')
        complete_form = self.complete_task_class(post_data, prefix='complete')

        context = self.get_context_data(create_form=create_form, update_form=update_form, complete_form=complete_form)

        if create_form.is_valid():
            self.form_create(create_form)
        else:
            messages.error(request, f'Something wrong with the form, here the post data: {request.POST}')
            return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')
        if update_form.is_valid():
            self.form_save(update_form)
        else: 
            messages.error(request, f'Something wrong with the form, here the post data: {request.POST}')
            return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')
        if complete_form.is_valid():
            self.form_save(complete_form)
        else: 
            messages.error(request, f'Something wrong with the form, here the post data: {request.POST}')
            return HttpResponseRedirect(f'/tables/tasks/{self.kwargs["key_id"]}')

    def form_create(self, form): 
        obj = form.save(commit=False)
        obj.created_by = request.user.id
        obj.date_created = datetime.now()
        obj.save()
        messages.success(self.request, '{} done!'.format(obj))
        return HttpResponseRedirect(f'rooms/')

    def form_update(self, form):
        obj = form.save(commit=False)
        # obj.
        messages.success(self.request, '{} done!'.format(obj))
        return obj

    def form_complete(self, form):
        obj = form.save(commit=False)
        # obj.
        messages.success(self.request, '{} done!'.format(obj))
        return obj
