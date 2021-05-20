from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib import messages
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required

from .models import (
    Room, Table, Task, Nessues_Group, 
    Nessues_Group_User, Invitation)
from .forms import (
    CreateRoomForm, CreateTableForm, CreateTaskForm, UpdateTaskForm, 
    CompleteTaskForm, DeleteRoomForm, CreateGroupForm, CloseGroupForm,
    AcceptInvitationForm, RefuseInvitationForm)


def home_view(request):
    title = "home"
    return render(request, 'nessues_app/home.html', {'title': title})


"""
 data that need to be rendered on the page: 
    1) title
    2) available_groups
    3) forms
        new group
"""
class GroupsView(TemplateView):
    template_name = 'nessues_app/groups.html'
    title = 'group'
    create_group_class = CreateGroupForm

    def get(self, request, *args, **kwargs):
        available_groups = Nessues_Group_User.objects.filter(user=self.request.user.id)
        create = self.create_group_class()
        return render(request, self.template_name, {'available_groups': available_groups, 'create': create})

    def post(self, request, *args, **kwargs):
        create = self.create_group_class(request.POST)

        if create.is_valid():
            create.save()
            current_group = Nessues_Group.objects.get(name=create.cleaned_data['name'])
            current_group.users.add(self.request.user.id, through_defaults={'role': 1})
            current_group.save()
            messages.success(request, "Group added")
            return HttpResponseRedirect('/groups')
        else:
            messages.warning(request, "Group with the same name already exists")
            return HttpResponseRedirect('/groups')
        return render(request, self.template_name, {'create': create})


"""
 data that need to be rendered on the page: 
    1) title
    2) available_rooms
    3) forms
        new room
"""
class RoomsView(TemplateView):
    template_name = 'nessues_app/mono_rooms.html'
    title = 'rooms'
    create_room_class = CreateRoomForm

    def get(self, request, *args, **kwargs):
        available_rooms = Room.objects.filter(owner=self.request.user.id)
        create = self.create_room_class(initial={'owner': self.request.user.id})

        return render(request, self.template_name, {'title': self.title, 'available_rooms': available_rooms, 'create': create})

    def post(self, request, *args, **kwargs):
        create = self.create_room_class(request.POST)

        if create.is_valid():
            create.save()
            return HttpResponseRedirect('/rooms')
        else: 
            messages.warning(request, "Something went wrong while creating room")
            return HttpResponseRedirect('/rooms')

        return render(request, self.template_name, {'create': create})


class TablesView(TemplateView):
    template_name = 'nessues_app/tables.html'
    title = 'tables'
    create_table_class = CreateTableForm
    delete_room_class = DeleteRoomForm
    close_group_class = CloseGroupForm

    def get(self, request, *args, **kwargs):
        if self.kwargs['redirected_from'] == 'group':
            try:
                current = Nessues_Group.objects.get(id=(self.kwargs['key_id']))
                try:
                    available_tables = Table.objects.filter(group=current.id)
                except:
                    available_tables = None
                create = self.create_table_class(initial={'group': current.id})
                delete = self.close_group_class(initial={'group': self.kwargs['key_id']})
            except:
                pass
        
        if self.kwargs['redirected_from'] == 'room':
            try:
                current = Room.objects.get(id=self.kwargs['key_id'])
                try:
                    available_tables = Table.objects.filter(room=current.id)
                except:
                    available_tables = None
                create = self.create_table_class(initial={'room': self.kwargs['key_id']})
                delete = self.delete_room_class(initial={'room': self.kwargs['key_id']})
            except:
                pass
        
        return render(request, self.template_name, {'title': self.title, 'current_type': self.kwargs['redirected_from'], 'current': current.id, 'current_name': current.name, 'available_tables': available_tables, 'create': create, 'delete': delete})
        

    def post(self, request, *args, **kwargs):
        create = self.create_table_class(request.POST)
        delete = self.delete_room_class(request.POST)

        if create.is_valid():
            create.save()
            return HttpResponseRedirect(f"/tables/{self.kwargs['redirected_from']}/{self.kwargs['key_id']}")
        
        if delete.is_valid():
            id_to_delete = delete.cleaned_data['id']
            current_room = (Room.objects.get(id=self.kwargs['key_id'])).id

            if current_room != id_to_delete:
                messages.warning(request, "You were restricted to delete other room")
                return HttpResponseRedirect(f'/tables/{self.kwargs["key_id"]}')
            try:    
                room_to_delete = Room.objects.get(id=id_to_delete) 
                room_to_delete.delete()
                messages.success(request, "Room deleted successfully")
                return HttpResponseRedirect('/rooms')
            except Exception:
                messages.warning(request, 'Wrong id provided, try again')
                return HttpResponseRedirect('/rooms')

        return render(request, self.template_name, {'create': create, 'delete': delete})


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
            return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')

        if update.is_valid():
            update.save()
            messages.success(request, 'Task successfully updated')
            return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')

        if complete.is_valid():
            id_to_close = complete.cleaned_data['id']
            try:    
                task_to_complete = Task.objects.get(id=id_to_close) 
                task_to_complete.delete()
            except Exception:
                messages.warning(request, 'Wrong id provided, try again')
                return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')

            messages.success(request, 'Task successfully completed')
            return HttpResponseRedirect(f'/tasks/{self.kwargs["key_id"]}')
        
        return render(request, self.template_name, {'create': create, 'update': update, 'complete': complete})


"""
 Forms to handle:
    1) accept invitation;
    2) refuse invitation.
"""
class InvitationsView(ListView): 
    model = Invitation
    template_name = "nessues_app/invitations.html"

    # def get(self, request, *args, **kwargs):
    #     # self.AcceptInvitationForm(self.request.GET or None)
    #     # self.RefuseInvitationForm(self.request.GET or None)
    #     return super(list(), self).get(request, *args, **kwargs)
    
    def get_queryset(self):
        try:        
            queryset = self.model.objects.get(user=self.request.user.id)
        except:
            return None
        return queryset

def about_view(request):
    content = {  }

    title = "about"
    return render(request, 'nessues_app/about.html', {'title': title, 'content': content})