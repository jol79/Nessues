from django import forms
from django.forms import CharField, HiddenInput, BooleanField, IntegerField
from .models import Room, Table, Task


class CreateRoomForm(forms.ModelForm):
    name = CharField(max_length=21)
    description = CharField(max_length=32)

    class Meta:
        model = Room
        fields = ['name', 'description', 'owner']
        widgets = {'owner': forms.HiddenInput()}

class CreateTableForm(forms.ModelForm):
    name = CharField(max_length=21)
    description = CharField(max_length=60)

    class Meta:
        model = Table
        fields = ['name', 'description', 'room', 'group']
        widgets = {'room': forms.HiddenInput(), 'group': forms.HiddenInput()}

class CreateTaskForm(forms.ModelForm): 
    text = CharField(max_length=120)

    class Meta:
        model = Task
        fields = ['text', 'completed', 'created_by', 'table']
        widgets = {'completed': forms.HiddenInput(), 'created_by': forms.HiddenInput(), 'table': forms.HiddenInput()}

