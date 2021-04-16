from django import forms
from django.forms import CharField, HiddenInput
from .models import Room, Table


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